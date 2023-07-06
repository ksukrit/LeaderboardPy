import os
import sys
import pandas as pd
import time
from timer import getTime
from eval import Evaluator
import constants
import schedule


def func():
    codes_dir = './submissions'
    df = pd.read_csv('leaderboard.csv', index_col=0)
    print(df.columns)

    # Get all list of groups
    groups = [d for d in os.listdir(codes_dir)]

    print("List of groups are :")
    print(groups)

    for group in groups:
        parentPath = codes_dir + '/' + group
        # Use this to run all the files in the directory
        # c_files = [c_files for c_files in os.listdir(parentPath)]

        # Use this to enforce specific naming convention in the assignment
        c_files = [group+"_assignment1.c"]
        print("------------------------------------------------------")
        print("\t Currently testing " + c_files[0] )
        print("------------------------------------------------------\n")
        for c_file in c_files:
            filepath = parentPath + '/' + c_file
            eval = Evaluator(filepath)
            s = eval.compile([],[])
            t = 0
            if s == constants.FILE_COMPILATION_FAILED:
                print("Compilation failed")
                status = constants.FILE_COMPILATION_FAILED
                t = 999999
        
            correctness = eval.runAllTestCases()
            if correctness == False:
                status = constants.TEST_CASES_FAILED
                t = 999999
            else:
                status = constants.FILE_PASSED
            
            lastRunTime = time.strftime('%l:%M%p %b %d') 
            group = group.split('.')[0]
            print("Running tests for group ", group, "/n")

            if status is constants.FILE_PASSED:
                # now time the program here
                t = getTime(constants.TIMEOUT,constants.LARGE_TEST_CASE_INPUT_ARGS)
                print(group + ' passed successfully with runtime: ' + str(t) + ' ms\n')
                print('Updating ', group, 'runtime')

                col_runtime = 'Time'
                print('Group type:', type(group))
                if group in df['GName'].values:
                    df.loc[df["GName"] == group, "Time"] = t
                    df.loc[df["GName"] == group, "Remarks"] = ['pass']
                    df.loc[df["GName"] == group, "LastRun"] = lastRunTime
                    
                else:
                    new_row = {'GName': [str(group)], 'Time': [float(t)], 'Remarks': ['pass'], 'LastRun':[lastRunTime]}
                    df_new = pd.DataFrame(new_row)
                    df = pd.concat([df, df_new], ignore_index=True, axis=0)
            elif status is constants.FILE_COMPILATION_FAILED: 
                print(filepath + ' failed to compile')
                if group in df['GName'].values:
                    df.loc[df["GName"] == group, "Time"] = t
                    df.loc[df["GName"] == group, "Remarks"] = "Compile Error or Wrong File Name or File Not Found"
                    df.loc[df["GName"] == group, "LastRun"] = lastRunTime
                else:
                    new_row = {'GName': [str(group)], 'Time': [float(t)], 'Remarks': ['Compile Error or Wrong File Name or File Not Found'], 'LastRun':[lastRunTime]}
                    df_new = pd.DataFrame(new_row)
                    df = pd.concat([df, df_new], ignore_index=True, axis=0)
            elif status is constants.TEST_CASES_FAILED:
                print(filepath + ' Test case didnt match')
                if group in df['GName'].values:
                    df.loc[df["GName"] == group, "Time"] = t
                    df.loc[df["GName"] == group, "Remarks"] = "Wrong Answer"
                    df.loc[df["GName"] == group, "LastRun"] = lastRunTime
                else:
                    new_row = {'GName': [str(group)], 'Time': [float(t)], 'Remarks': ['Wrong Answer'], 'LastRun':[lastRunTime]}
                    df_new = pd.DataFrame(new_row)
                    df = pd.concat([df, df_new], ignore_index=True, axis=0)
            
            df.sort_values('Time', inplace=True)
            df.to_csv('leaderboard.csv')
            
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python3 main.py <once|regular> <optional: interval>')
        exit(1)
    
    if sys.argv[1] == 'once':
        func()
        exit(0)
    elif sys.argv[1] == 'regular':
        print(f"Running in loop with time inverval {sys.argv[2]} minutes")
        schedule.every(int(sys.argv[2])).minutes.do(func)
        while True:
            schedule.run_pending()
            time.sleep(1)
