#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>
     
// can be made local if required
int N;
     
// Helper struct, can utilize any other custom structs if needed
typedef struct
{
  int x, y;
} pair;
     
static pair dir[8] = {{ 2, 1}, { 1, 2}, {-2, 1}, {-1, 2},
							 				{-2,-1}, {-1,-2}, { 2,-1}, { 1,-2}};
							 
// Not necessary to use this function as long as same printing pattern is followed
void print_path(pair path[], int n)
{
  for (int i = 0; i < n; i++)
  {
    printf("%d,%d|", path[i].x, path[i].y);
  }
}

int is_valid(int board[][N], int x, int y)
{
	return ((x>=0 && x<N && y>=0 && y<N) && board[x][y]==-1);
}

int freeNeighbours(int board[][N], int x, int y)
{
	int cnt = 0;
		for(int i = 0; i<8; i++)
			if(is_valid(board, x+dir[i].x, y+dir[i].y))
				cnt++;
	return cnt;
}

int warnsdorffsHeuristic(int board[][N], int *x, int *y)
{
	int min = 9, mini = -1, cur, xx, yy;
	int rpick = rand()%8;
	
	for(int i=0; i<8; i++){
		int j=(i+rpick)%8;
		xx = *x + dir[j].x;
		yy = *y + dir[j].y;
		
		if(is_valid(board, xx, yy) && (cur = freeNeighbours(board, xx, yy))<min){
			min = cur,mini = j;
		}
	}
	
	if(mini == -1)
		return 0;
		
	xx = *x + dir[mini].x, yy = *y + dir[mini].y;
	
	board[xx][yy] = board[*x][*y]+1;
	
	*x = xx, *y = yy;
	
	return 1;
}

unsigned long mixJenkins(unsigned long a, unsigned long b, unsigned long c)
{
	a=a-b;  a=a-c;  a=a^(c >> 13);
	b=b-c;  b=b-a;  b=b^(a << 8);
  c=c-a;  c=c-b;  c=c^(b >> 13);
  a=a-b;  a=a-c;  a=a^(c >> 12);
  b=b-c;  b=b-a;  b=b^(a << 16);
  c=c-a;  c=c-b;  c=c^(b >> 5);
  a=a-b;  a=a-c;  a=a^(c >> 3);
  b=b-c;  b=b-a;  b=b^(a << 10);
  c=c-a;  c=c-b;  c=c^(b >> 15);
  return c;
}
 
int main(int argc, char *argv[])
{
    
 
  N = 3;
  int StartX = 1;
  int StartY = 1;
 	
  /* Do your thing here */
  if(N<5 || (N%2==1 && (StartX+StartY)%2==1))
  {
  	if(N==1)
  		printf("0,0|");
  	else
  		printf("No Possbile Tour");
  	return 0;
  }
  srand(mixJenkins(clock(), time(NULL), getpid()));
  
  int board[N][N];
  pair path[N*N];
  int t=1;
  
  while(t)
  {
		memset(board, -1, sizeof(board));
		
		board[StartX][StartY] = 0;
		int x=StartX, y=StartY;
		t=0;
		for(int i=0; i<N*N-1; i++)
			if(warnsdorffsHeuristic(board, &x, &y)==0){
				t = 1;
				continue;
			}
	}
  
  for(int i=0; i<N; i++)
  {
  	for(int j=0; j<N; j++)
  	{
  		path[board[i][j]].x = i;
  		path[board[i][j]].y = j;
  	}
  }
	
	print_path(path, N*N);
	
  return 0;
}