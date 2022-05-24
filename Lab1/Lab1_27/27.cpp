/* Assignment: 01, Team no: 27 , Name: Karthik JP , Roll no: 200010022, Name: Pavan Kumar V Patil , Roll no: 200030041 */
#include<bits/stdc++.h>
#include<stdio.h>
#include<stdlib.h>

using namespace std;

class vertex {
    public:
        char sym;
        pair<int, int> parent;
        vector<pair<int,int>> adjNodes;
};

int m,n,run;
int flag=0;
int goalX, goalY;

vertex** info = NULL;
int** visited = NULL;

int BFSlength = 1;
int BFSstates = 1;

int DFSlength = 1;
int DFSstates = 1;

int DFIDstates = 1;
int DFIDlength = 1;

vector<int> readFile()
{
    FILE *fp;
    int run,m=0,n=0,flag_=0;
    char c,c_check;
    vector<int> input;
    fp = fopen("input.txt","r");
    c_check = run + 48;
    fscanf(fp,"%d\n",&run);
    while(1)
    {
        fscanf(fp,"%c",&c);
        if(feof(fp))
        {
            if(c_check != '\n')
                m++;
            break;
        }
        else if(c == '\n')
        {
            flag_ = 1;
            if(c_check == '\n')
            {
                break;
            }
            else
            {
                m++;
            }
        }
        if(flag_ == 0)
        {
            n++;
        }
        c_check = c;
    }
    fclose(fp);
    input.push_back(run);
    input.push_back(m);
    input.push_back(n);
    return input;
}

void createGraph() {
    for(int i=0; i<m; i++) {
        for(int j=0; j<n; j++)
        {
            if ( info[i][j].sym == ' ')
            {
                if ( i+1 < m ) {
                    if ( info[i+1][j].sym == ' ') {
                        info[i][j].adjNodes.push_back({i+1, j});
                    }
                }
                if( i-1 >= 0 ) {
                    if( info[i-1][j].sym == ' ' ) {
                        info[i][j].adjNodes.push_back({i-1, j});
                    }
                }
                if ( j+1 < n ) {
                    if( info[i][j+1].sym == ' ') {
                        info[i][j].adjNodes.push_back({i, j+1});
                    }
                }
                if ( j-1 >= 0 ) {
                    if( info[i][j-1].sym == ' ') {
                        info[i][j].adjNodes.push_back({i, j-1});
                    }
                }
            }

        }
    }
}

vector<pair<int,int>> moveGen(pair<int,int> node) {
    vector<pair<int,int>> ans;
    for ( auto i : info[node.first][node.second].adjNodes) {
        ans.push_back(i);
    }
    return ans;
}
bool goalTest(pair<int, int> node) {
    if( node.first == goalX && node.second == goalY ) {
        return true;
    }
    return false;
}

void BFS() {
    queue<pair<int,int>> remain;
    remain.push({0,0});
    visited[0][0] = 1;
    info[0][0].sym = '0';
    while ( remain.size() != 0 ) {
        pair<int,int> current = remain.front();
        remain.pop();
        vector<pair<int,int>> adjNodes = moveGen(current);
        for ( auto node : adjNodes ) {
            if( !visited[node.first][node.second] ) {
                if ( goalTest(node) ) {
                    info[goalX][goalY].sym= '0';
                    info[node.first][node.second].parent.first = current.first;
                    info[node.first][node.second].parent.second = current.second;
                    BFSstates++;
                    return;
                }
                remain.push(node);
                info[node.first][node.second].parent.first = current.first;
                info[node.first][node.second].parent.second = current.second;
                visited[node.first][node.second] = 1;
                BFSstates++;
            }
        }
    }
}
void DFS(pair<int,int> start)
{
    pair<int,int> current = start;
    vector<pair<int,int>> adjNodes = moveGen(start);
    if( adjNodes.size() == 0 )
    {
        if( goalTest(start) )
        {
            flag=1;
            info[start.first][start.second].parent.first = current.first;
            info[start.first][start.second].parent.second = current.second;
            visited[start.first][start.second] = 1;
            info[start.first][start.second].sym = '0';
            DFSstates++;
        }
        visited[start.first][start.second] = 1;
        return;
    }
    for ( auto node : adjNodes ) {
        if( !visited[node.first][node.second] )
        {
            if( goalTest(node) )
            {
                visited[node.first][node.second] = 1;
                info[node.first][node.second].parent.first = current.first;
                info[node.first][node.second].parent.second = current.second;
                info[node.first][node.second].sym = '0';
                DFSstates++;
                flag=1;
                return;
            }
            visited[node.first][node.second] = 1;
            info[node.first][node.second].parent.first = current.first;
            info[node.first][node.second].parent.second = current.second;
            if (flag==0)
            {
                DFSstates++;
                DFS(node);
            }
        }
    }
}

void DFSrestricted(pair<int, int> start, int depth) {
    pair<int,int> current = start;
    vector<pair<int,int>> adjNodes = moveGen(start);
    if( depth == 0 ) {
        if ( goalTest(start) ) {
            flag = 1;
            info[goalX][goalY].sym = '0';
            info[start.first][start.second].parent.first = current.first;
            info[start.first][start.second].parent.second = current.second;
            DFIDstates++;
            visited[start.first][start.second] = 1;
            return;
        }
        visited[start.first][start.second] = 1;
        return;
    }
    for( auto node : adjNodes ) {
        if ( !visited[node.first][node.second] ) {
            visited[node.first][node.second]=1;
            if( goalTest(node)) {
                flag = 1;
                info[node.first][node.second].parent.first = current.first;
                info[node.first][node.second].parent.second = current.second;
                DFIDstates++;
                info[goalX][goalY].sym = '0';
                return;
            }
            info[node.first][node.second].parent.first = current.first;
            info[node.first][node.second].parent.second = current.second;
            if ( flag == 0 ) {
                DFIDstates++;
                DFSrestricted(node, depth-1);
            }
        }
    }
}
void DFID() {
    for( int i=0; ; i++) {
        for ( int i=0; i<m; i++ ) {
            for ( int j=0; j<n; j++) {
                visited[i][j] = 0;
            }
        }
        flag = 0;
        info[0][0].sym = '0';
        DFSrestricted({0, 0}, i);
        if ( flag == 1 ){
            break;
        }
    }
}

void BFSpath(){
    int i = goalX, j = goalY;
    while( i!=0 || j!=0 ) {
        pair<int, int> parent;
        parent.first = info[i][j].parent.first;
        parent.second = info[i][j].parent.second;
        BFSlength++;
        info[i][j].sym = '0';
        i = parent.first;
        j = parent.second;
    }
}
void DFSpath()
{
    int i = goalX, j = goalY;
    while (i != 0 || j != 0)
    {
        pair<int, int> parent;
        parent.first = info[i][j].parent.first;
        parent.second = info[i][j].parent.second;
        DFSlength++;
        info[i][j].sym = '0';
        i = parent.first;
        j = parent.second;
    }
}
void DFIDpath()
{
    int i = goalX, j = goalY;
    while (i != 0 || j != 0)
    {
        pair<int, int> parent;
        parent.first = info[i][j].parent.first;
        parent.second = info[i][j].parent.second;
        DFIDlength++;
        info[i][j].sym = '0';
        i = parent.first;
        j = parent.second;
    }
}

int main()
{
    vector<int> input;
    char sym;
    input = readFile();
    run = input[0];
    m = input[1];
    n = input[2];
    FILE* ptr = fopen("input.txt", "r");
    fscanf(ptr,"%d\n",&run);
    info = new vertex*[m];
    for ( int i=0; i<m; i++ ) {
        info[i] = new vertex[n];
        for ( int j=0; j<n; j++ ) {
            fscanf(ptr, "%c", &sym);
            if(sym == '*') {
                goalX = i;
                goalY = j;
                info[i][j].sym = ' ';
                info[i][j].parent.first = -1;
                info[i][j].parent.second = -1;
                continue;
            }
            info[i][j].sym = sym;
            info[i][j].parent.first = -1;
            info[i][j].parent.second = -1;
        }
        char temp;
        fscanf(ptr,"%c",&temp);
    }
    info[0][0].sym = ' ';
    createGraph();

    visited = (int **)malloc(sizeof(int *) * m);
    for( int i=0; i<m; i++ ) {
        visited[i] = (int *)malloc(sizeof(int) * n);
        for( int j=0; j<n; j++ ) {
            visited[i][j] = 0;
        }
    }

    info[0][0].sym = '0';
    if(run == 0)
    {
        BFS();
        BFSpath();
        cout<<BFSstates<<endl;
        cout<<BFSlength<<endl;
    }
    else if(run == 1)
    {
        DFS({0, 0});
        DFSpath();
        cout<<DFSstates<<endl;
        cout<<DFSlength<<endl;
    }
    else if(run == 2)
    {
        DFID();
        DFIDpath();
        cout<<DFIDstates<<endl;
        cout<<DFIDlength<<endl;
    }
    for (int i=0; i<m; i++) {
        for (int j=0; j<n; j++) {
            printf("%c", info[i][j].sym);
        }
        printf("\n");
    }
    return 0;
}
