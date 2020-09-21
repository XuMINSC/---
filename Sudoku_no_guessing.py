import pandas as pd
import numpy as np


class Sudoku:
    def __init__(self, sudoku):
        self.sudoku = sudoku
    
    def cell_location(self, i, j):
        cell = 0
        if i in [0,1,2] and j in [0,1,2]:
            cell = 0
        elif i in [0,1,2] and j in [3,4,5]:
            cell = 1
        elif i in [0,1,2] and j in [6,7,8]:
            cell = 2
        elif i in [3,4,5] and j in [0,1,2]:
            cell = 3
        elif i in [3,4,5] and j in [3,4,5]:
            cell = 4
        elif i in [3,4,5] and j in [6,7,8]:
            cell = 5
        elif i in [6,7,8] and j in [0,1,2]:
            cell = 6
        elif i in [6,7,8] and j in [3,4,5]:
            cell = 7
        else:
            cell = 8
        return(cell)
    
    def cell_ins(self,i):
        if i == 0:
            return(set(np.array(self.sudoku.iloc[0:3,0:3]).flatten()))
        elif i == 1:
            return(set(np.array(self.sudoku.iloc[0:3,3:6]).flatten()))
        elif i == 2:
            return(set(np.array(self.sudoku.iloc[0:3,6:9]).flatten()))
        if i == 3:
            return(set(np.array(self.sudoku.iloc[3:6,0:3]).flatten()))
        elif i == 4:
            return(set(np.array(self.sudoku.iloc[3:6,3:6]).flatten()))
        elif i == 5:
            return(set(np.array(self.sudoku.iloc[3:6,6:9]).flatten()))
        if i == 6:
            return(set(np.array(self.sudoku.iloc[6:9,0:3]).flatten()))
        elif i == 7:
            return(set(np.array(self.sudoku.iloc[6:9,3:6]).flatten()))
        else:
            return(set(np.array(self.sudoku.iloc[6:9,6:9]).flatten()))
    
    def cell_coors(self,i):
        if i == 0:
            return([[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]])
        if i == 1:
            return([[0,3],[0,4],[0,5],[1,3],[1,4],[1,5],[2,3],[2,4],[2,5]])
        if i == 2:
            return([[0,6],[0,7],[0,8],[1,6],[1,7],[1,8],[2,6],[2,7],[2,8]])

        if i == 3:
            return([[3,0],[3,1],[3,2],[4,0],[4,1],[4,2],[5,0],[5,1],[5,2]])
        if i == 4:
            return([[3,3],[3,4],[3,5],[4,3],[4,4],[4,5],[5,3],[5,4],[5,5]])
        if i == 5:
            return([[3,6],[3,7],[3,8],[4,6],[4,7],[4,8],[5,6],[5,7],[5,8]])

        if i == 6:
            return([[6,0],[6,1],[6,2],[7,0],[7,1],[7,2],[8,0],[8,1],[8,2]])
        if i == 7:
            return([[6,3],[6,4],[6,5],[7,3],[7,4],[7,5],[8,3],[8,4],[8,5]])
        if i == 8:
            return([[6,6],[6,7],[6,8],[7,6],[7,7],[7,8],[8,6],[8,7],[8,8]])
    
    def pools_solve(self):
        count = 0
        for i in range(0,9):
            for j in range(0,9):
                full = {0,1,2,3,4,5,6,7,8,9}

                if self.sudoku.iloc[i,j] == 0:
                    rowpool = full - set(self.sudoku.iloc[i,:]) - {0}
                    colpool = full - set(self.sudoku.iloc[:,j]) - {0}
                    cellpool = full - self.cell_ins(self.cell_location(i,j)) - {0}

                    pool = rowpool & colpool & cellpool
                    if len(pool) == 1:
                        count += 1
                        a = pool.pop()
                        #print('把{}放到[{}, {}]'.format(a,i,j))
                        self.sudoku.iloc[i,j] = a
        if count > 0:
            return('Yes',count)
        else:
            return('No')
    
    def ending(self):
        for i in range(0,9):
            full = {0,1,2,3,4,5,6,7,8,9}
            if full - self.cell_ins(i)-{0} != set():
                return('No')#还可以考虑添加限制条件
        return('Yes')
    
    def cross(self):
        #创造一堆容器来盛放中间变量
        for i in range(1,10):
            exec('cor{} = []'.format(i))
            exec('row{} = []'.format(i))
            exec('col{} = []'.format(i))

        full = {0,1,2,3,4,5,6,7,8}

        for num in range(1,10): #数字1-10
            for row in range(0,9): #第0-8行
                try:
                    col = list(self.sudoku.iloc[row,:]).index(num)
                    eval('cor{}'.format(num)).append([row,col])
                    #确定数字num在数独中的坐标并放入容器
                except:
                    continue

    #     for num in range(1,10):
    #         print(eval('cor{}'.format(num)))#查看每个num在数独中的坐标

        for num in range(1,10):
            for coordinates in eval('cor{}'.format(num)):
                eval('row{}'.format(num)).append(coordinates[0]) #确定每个num已经出现的行
                eval('col{}'.format(num)).append(coordinates[1]) #确定每个num已经出现的列

        for num in range(1,10):
            exec('acor{} = []'.format(num))
            exec('arow{} = full - set(row{})'.format(num,num)) #available rows:现有行的反集
            exec('acol{} = full - set(col{})'.format(num,num)) #available cols:现有列的反集

        for num in range(1,10):
            for row in eval('arow{}'.format(num)):
                for col in eval('acol{}'.format(num)):
                    eval('acor{}'.format(num)).append([row,col]) 
                    #根据available rows/cols初步确定available coordinates   

        for num in range(1,10):
            exec('now_cells{} = []'.format(num)) #空容器：放入现有每个num所在的cell编号
            exec('new_cells{} = []'.format(num)) #空容器：放入剩余每个num潜在的cell编号
            exec('last_cor{} = []'.format(num)) #空容器：放入剩余每个num潜在的cell坐标筛选后)

        for num in range(1,10):
            for coordinates in eval('cor{}'.format(num)):
                eval('now_cells{}'.format(num)).append(self.cell_location(coordinates[0],coordinates[1]))
                #放入现有每个num的cell编号

        count = 0
        for num in range(1,10):
            for coordinates in eval('acor{}'.format(num)):
                if self.cell_location(coordinates[0],coordinates[1]) not in eval('now_cells{}'.format(num)) and self.sudoku.iloc[coordinates[0],coordinates[1]] == 0:
                    #条件一：不能出现在已有cell
                    #条件二：该位置必须是空白（0）

                    eval('last_cor{}'.format(num)).append(coordinates)
                    eval('new_cells{}'.format(num)).append(self.cell_location(coordinates[0],coordinates[1]))

            for i in eval('new_cells{}'.format(num)):
                 if eval('new_cells{}'.format(num)).count(i) == 1:
                        obj = eval('last_cor{}'.format(num))[eval('new_cells{}'.format(num)).index(i)]
                        print('把{}放到{}'.format(num,obj))
                        self.sudoku.iloc[obj[0],obj[1]] = num
                        count += 1
            return(count)
    
    def cross_eliminate(self):
        for i in range(1,10):
            exec('pool_of_{} = []'.format(i))
            exec('from_pool_{} = []'.format(i))
            exec('lucky_box_{} = []'.format(i))
            exec('occued_rows_of_{} = []'.format(i))
            exec('occued_cols_of_{} = []'.format(i))#1-9的容纳池
        
        for num in range(1,10):
            for i in range(0,9):
                for j in range(0,9):
                    if self.sudoku.iloc[i,j] == num:
                        eval('occued_rows_of_{}'.format(num)).append(i)
                        eval('occued_cols_of_{}'.format(num)).append(j)

        for num in range(1,10):
            for cell_num in range(0,9):
                if num in self.cell_ins(cell_num):
                    pass
                else:
                    eval('pool_of_{}'.format(num)).append(cell_num)#找到仍未有该num出现的cell

        #进一步判断并找出这些cell中的空格
        for i in range(1,10):
            for cell_num in eval('pool_of_{}'.format(i)):
                for j in self.cell_coors(cell_num):
                    if self.sudoku.iloc[j[0],j[1]] == 0:
                        if j[0] not in eval('occued_rows_of_{}'.format(i)) and j[1] not in eval('occued_cols_of_{}'.format(i)):
                            eval('from_pool_{}'.format(i)).append(j)
                    else:
                        pass

        for i in range(1,10):
            for j in eval('from_pool_{}'.format(i)):
                          eval('lucky_box_{}'.format(i)).append(self.cell_location(j[0],j[1]))

            for p in eval('lucky_box_{}'.format(i)):
                obj = eval('lucky_box_{}'.format(i)).count(p)
                if obj == 1:
                    where = eval('from_pool_{}'.format(i))[eval('lucky_box_{}'.format(i)).index(p)]
                    print('把{}放到{}'.format(i,where))
                    self.sudoku.iloc[where[0],where[1]] = i

    def threed(self):
        for num in range(1,10):
            for i in range(0,9):
                for j in range(0,9):
                    if self.sudoku.iloc[i,j] == 0:
                        ##放入同行和同列的坐标,像一个十字路口

                        #先来行方向
                        junction_heng = [[i,q] for q in range(0,9)]#用列表解析式简化一下
                        blank_junction_heng = []
                        for x in junction_heng:
                            if self.sudoku.iloc[x[0],x[1]] == 0:
                                blank_junction_heng.append(x)#只留下值为空的坐标
                        available_heng = []
                        for y in blank_junction_heng:
                            heng1 = set(self.sudoku.iloc[y[0],:])#横轴已出现的值
                            shu1 = set(self.sudoku.iloc[:,y[1]])#纵轴已出现的值
                            cell1 = self.cell_ins(self.cell_location(y[0],y[1]))#cell已出现的值
                            all1 = heng1 | shu1 | cell1
                            if num in all1:
                                pass
                            else:
                                available_heng.append(y)#选出所在行/列/cell均未出现num的空格，仿佛available备选       
                        if len(available_heng) == 1:
                            ver = available_heng[0][0]
                            hor = available_heng[0][1]
                            self.sudoku.iloc[ver,hor] = num
                            print('Yes!在{}放入{}来自[{}, {}]横向'.format(available_heng[0],num,i,j))

                        #再来列方向 
                        junction_shu = [[p,j] for p in range(0,9)]
                        blank_junction_shu = []
                        for x in junction_shu:
                            if self.sudoku.iloc[x[0],x[1]] == 0:
                                blank_junction_shu.append(x)#只留下值为空的坐标
                        available_shu = []
                        for y in blank_junction_shu:
                            heng2 = set(self.sudoku.iloc[y[0],:])#横轴已出现的值
                            shu2 = set(self.sudoku.iloc[:,y[1]])#纵轴已出现的值
                            cell2 = self.cell_ins(self.cell_location(y[0],y[1]))#cell已出现的值
                            all2 = heng2 | shu2 | cell2
                            if num in all2:
                                pass
                            else:
                                available_shu.append(y)#选出所在行/列/cell均未出现num的空格，仿佛available备选       
                        if len(available_shu) == 1:
                            ver = available_shu[0][0]
                            hor = available_shu[0][1]
                            self.sudoku.iloc[ver,hor] = num
                            print('Yes!在{}放入{}来自[{}, {}]竖向'.format(available_shu[0],num,i,j))

def solve(sudoku):
    mx = Sudoku(sudoku)
    for i in range(0,10):
        mx.cross_eliminate()
        mx.pools_solve()
        mx.cross()
        mx.threed()
    print(mx.ending())
    print(mx.sudoku)

sudoku_raw = input('PLZ ENTER LINE the Sudoku (Separated by wide spaces): ')
sudoku_pieces = sudoku_raw.split(' ')
for i in range(0,len(sudoku_pieces)):
    exec('c{} = [int(j) for j in sudoku_pieces[{}]]'.format(i+1,i))

sudoku = pd.DataFrame({'c1':c1,
                      'c2':c2,
                      'c3':c3,
                      'c4':c4,
                      'c5':c5,
                      'c6':c6,
                      'c7':c7,
                      'c8':c8,
                      'c9':c9})
sudoku.index = ['r1','r2','r3','r4','r5','r6','r7','r8','r9']
solve(sudoku)
