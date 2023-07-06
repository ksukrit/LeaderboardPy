import os
from subprocess import Popen, PIPE, call
import os
import platform
import sys
import constants

class Validator:
    def validate(self):
        pass

# Custom Validator writen for the Knight's tour problem
class CustomOutputValidator(Validator):    
    def __init__(self, input, output):
        self.input = input
        self.output = output

    # Validate if the knight made a valid move in the solution
    def validateMove(self,currentpos,nextpos):
        currentpos = currentpos.split(',')
        nextpos = nextpos.split(',')
        xdiff = abs(int(currentpos[0]) - int(nextpos[0]))
        ydiff = abs(int(currentpos[1]) - int(nextpos[1]))
        return (xdiff == 2 and ydiff == 1) or (xdiff == 1 and ydiff == 2)
    
    def validate(self):
        moves = self.output.split('|');
        moves = moves[:-1]
        # print("moves",moves);
        if len(moves) == 0:
            return False
        prev = moves[0]
        moves_set = {prev}
        res = True
        for i in range(1, len(moves)):
            curr = moves[i]
            if not self.validateMoves(prev,curr):
                res = False
                break
            prev = curr
            moves_set.add(curr)
        print(moves_set)
        print(len(moves_set))
        res &= len(moves_set) == int(self.input[0])*int(self.input[0])
        print("Moves are valid and reaches all cells : ", res)
        return res


class Evaluator:
    def __init__(self,filepath,tests_dir = 'test_cases') -> None:
        self.test_dir = tests_dir
        self.test_cases = os.listdir(tests_dir)
        self.filepath = filepath

    def compile(self,pre_flags,post_flags):
        if len(pre_flags) == 0:
            pre_flags = ['gcc']
        else:
            pre_flags = ['gcc'] + pre_flags
        if len(post_flags) == 0:
            post_flags = []
        cmd = pre_flags + [self.filepath] + post_flags
        print("Compiling with command ",cmd)
        compile_status = call(['gcc','-pthread',self.filepath, '-lm'])  # Need to check for compilation error
        if compile_status == 0 :
            print('\nCompilation successful: ' + self.filepath)
            return constants.FILE_PASSED
        else: 
            # t=999999999
            return constants.FILE_COMPILATION_FAILED

    def readFileToString(self,filepath):
        with open(filepath, 'r') as file:
            data = file.read()  # .replace('\n', '')
            return data

    def runTestCase(self,input_path,output_path):
        input = self.readFileToString(input_path)
        input = input.split()

        platf = platform.system()
        if platf == "Windows":
            cmd = "a.exe"
        elif platf == "Linux" or platf == "Darwin":
            cmd = "timeout 1m ./a.out"
        else:
            print("Unidentified System")
            return False
        
        p = Popen([cmd]+input, stdout=PIPE).communicate() #.communicate(c_input.encode('utf-8'))
        c_output = p[0].decode('utf-8')
        expected_output = self.readFileToString(output_path)

        # If we have ignore in the expected text file we will not compare the output instead we will just check if the output is valid using methods
        # Like in the Knight's tour case there can be multiple solutions
        if not "Ignore" in expected_output:
            print("Program output is : \n",c_output)
            print("expected_output",expected_output)
            if c_output != expected_output:
                print("Error")
                return False
            else:
                print("Output matches as expected ")
                return True
        c_output = c_output.split()
        print("Program output is :\n", c_output[0])
        output = c_output[0]
        validator = CustomOutputValidator(input,output)
        res = validator.validate()
        
        sys.stdout.flush()
                    
        return res

    def runAllTestCases(self,filepath):
        for case in self.test_cases:
            print("Running test case ", case)
            input_path = self.test_dir + '/' + case + '/input.txt'
            output_path = self.test_dir + '/' + case + '/output.txt'
            is_test_passed = self.runTestCase(input_path,output_path)

            group = filepath.split('/')[1]
            pass_count = 0

            if is_test_passed:
                pass_count += 1
                print(group + ' passed test ' + case + ' succesfully ✓')
            else:
                print(group + ' failed test ' + case + ' succesfully ✗')
                # Don't run the rest of the tests, we can
                return False
        print(group + ' passed ' + str(pass_count) + ' out of ' + str(len(self.test_cases)) + ' tests')
        return True