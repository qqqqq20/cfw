# 员工行为类
from employee import (Employee)
import os
import sqlite3


class EmployeeManagerSystem(object):
    def __init__(self):
        # 存放员工数据的文件
        self.employee_date_file = 'employee.data'
        # 上次保存前的员工备份文件，而且只备份一份
        self.employee_date_file_backup = 'employee.backup'
        # 从文件中加载到员工列表
        self.employee_list = []

        self.save_flag = True  # True表示已经保存数据了

    def main(self):
        """员工管理系统的入口"""
        # 1.加载和读取员工数据文件
        self.load_employee()
        # 2.显示欢迎界面
        while True:
            self.show_hello()
            try:
                menu_number = int(input('请输入你需要的功能编号: '))
            except ValueError:
                print('输入无效，请输入一个数字！')
                continue  # 跳过后续代码，重新开始循环
            if menu_number == 7:
                self.go_out()
                print('程序已退出')
                break
            elif menu_number < 0 or menu_number > 8:
                print('请输入正确的功能编号')
            elif menu_number == 1:
                self.add_employee()
            elif menu_number == 2:
                self.del_employee()
            elif menu_number == 3:
                self.update_employee()
            elif menu_number == 4:
                self.search_employee()
            elif menu_number == 5:
                self.show_employee()
            elif menu_number == 6:
                self.save_employee()
                print('已成功保存')
            elif menu_number == 8:
                self.sql_employee()
                print('已成功保存至数据库')

    def sql_employee(self):
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            name TEXT UNIQUE,
            gender TEXT CHECK(gender IN ('男', '女')),
            age INTEGER,
            mobile_number TEXT,
            is_leave TEXT CHECK(is_leave IN ('1', '0'))
        )
        ''')
        with open(self.employee_date_file, 'r', encoding='gbk') as f:
            r1 = f.readline()
            lst = eval(r1)  # 文件内容转字符串，供可解析
            for emp1 in lst:
                cursor.execute("SELECT name FROM users WHERE name = ?", (emp1['name'],))
                result = cursor.fetchone()

                if result:  # 更新
                    cursor.execute('UPDATE users SET gender = ?, age = ?, mobile_number = ?, is_leave = ? WHERE name '
                                   '= ?',
                                   (
                                       emp1['gender'], emp1['age'], emp1['mobile_number'],
                                       '1' if emp1['is_leave'] else '0',
                                       emp1['name'])
                                   )
                else:  # 添加
                    cursor.execute(
                        'INSERT INTO users (name, gender, age, mobile_number, is_leave) VALUES (?, ?, ?, ?, ?)',
                        (emp1['name'], emp1['gender'], emp1['age'], emp1['mobile_number'],
                         '1' if emp1['is_leave'] else '0')
                    )
                    # 获取文件中的员工名字
            file_names = {emp1['name'] for emp1 in lst}

            # 查询数据库中的员工名字
            cursor.execute("SELECT name FROM users")
            db_names = cursor.fetchall()
            db_names = {name[0] for name in db_names}  # 转换为集合以便比较

            # 删除数据库中不在文件中的记录
            for name in db_names:
                if name not in file_names:
                    cursor.execute("DELETE FROM users WHERE name = ?", (name,))

        conn.commit()  # 提交修改
        conn.close()  # 关闭连接

    def go_out(self):
        """提出程序的需求，如果，员工进行了添加，修改，删除，那么必须保存到文件中
        1.如果没有保存，则在退出之前自动保存
        2.先判断有没有保存
        """
        if not self.save_flag:
            self.save_employee()
            print('已自动保存')

    def save_employee(self):
        """
        保存前的需求和步骤
        1.先把原来的数据文件备份(如果已经存在备份文件，则把备份文件删除)
        2.创建新文件
        3.写入数据
        4.关闭文件
        :return:
        """
        if os.path.exists(self.employee_date_file_backup):
            os.remove(self.employee_date_file_backup)  # 删除备份文件
        # 1.备份
        os.rename(self.employee_date_file, self.employee_date_file_backup)
        # 2.打开文件流
        with open(self.employee_date_file, 'w', encoding='gbk') as f:
            # 3.写入数据
            new_list = []
            for emp in self.employee_list:  # 原来的列表中是一个个的emp对象
                new_list.append(emp.__dict__)
            # new_list:[{'name':'zs'},{},{},{},{}]
            f.write(str(new_list))
        self.save_flag = True

    def show_employee(self):
        """显示所有员工信息"""
        print('姓名\t年龄\t性别\t手机号码\t是否离职')
        for emp in self.employee_list:
            print(emp)

    def search_employee(self):
        """查找员工信息"""
        # 1输入需要查找员工的姓名
        search_name = input('请输入要查找的员工姓名')
        # 2.遍历员工信息
        for emp in self.employee_list:
            if emp.name == search_name:
                print(emp)
                break
        else:
            print(f'没有姓名为{search_name}员工')

    def update_employee(self):
        """修改员工信息"""
        # 1.输入需要修改员工的姓名
        update_name = input('请输入修改的员工姓名:')
        # 2.遍历员工列表
        for emp in self.employee_list:
            if emp.name == update_name:
                new_name = input('请输入新的姓名(不修改直接回车):').strip()  # .strip清除多余空白，可指定
                emp.name = new_name if new_name else emp.name

                new_gender = input('请输入新的性别(不修改直接回车):').strip()
                emp.gender = new_gender if new_gender else emp.gender

                new_age = input('请输入新的年龄(不修改直接回车):').strip()
                emp.age = int(new_age) if new_age else emp.age

                new_mobile_number = input('请输入新的手机号码(不修改直接回车):').strip()
                emp.mobile_number = new_mobile_number if new_mobile_number else emp.mobile_number

                new_is_leave = input('请输入是否离职,0表示在职，1表示离职(不修改直接回车):').strip()
                if new_is_leave:
                    emp.is_leave = True if int(new_is_leave) == 1 else False

                print('员工信息已修改完成：')
                print(emp)
                break
        else:  # 表示循环正式结束
            print(f'没有找到姓名为{update_name}的员工')
        self.save_flag = False

    def del_employee(self):
        """删除员工信息"""
        # 1.输入被删除员工的名字
        del_name = input('请输入需要删除的员工姓名:')
        # 2.遍历员工列表，判断是否存在，存在则删除
        for emp in self.employee_list:
            if emp.name == del_name:
                self.employee_list.remove(emp)
                print(f'名字叫:{del_name}的员工已被删除')
                break
        else:
            print(f'没有找到姓名为{del_name}的员工')
        self.save_flag = False

    def add_employee(self):
        """添加员工信息"""
        name = input('请输入员工的姓名：')
        gender = input('请输入员工的性别：')
        age = int(input('请输入员工的年龄：'))
        mobile_number = input('请输入员工的手机号码：')
        is_leave = int(input('请输入员工是否离职，1表示离职，0表示在职：'))

        # 2.创建一个员工对象
        emp = Employee(name, gender, age, mobile_number, is_leave)
        # 3.添加到列表中去
        self.employee_list.append(emp)
        # 4.把刚添加的员工信息，输出
        print(emp)
        self.save_flag = False

    @staticmethod
    def show_hello():
        # "系统欢迎界面"
        print('欢迎进入企业员工管理系统')
        print('-' * 60)
        print('1:添加员工')
        print('2:删除员工')
        print('3:修改员工')
        print('4:查找员工')
        print('5:展示所有员工')
        print('6:保存员工数据')
        print('7:退出系统')
        print('8:保存到数据库')

    def load_employee(self):
        # """
        # 读取员工数据文件，把所有员工信息都放到一个列表中
        # :return:
        # """

        try:
            f = open(self.employee_date_file, 'r', encoding='gbk')
        except ValueError:
            # 如果报错，文件不存在需要创建一下
            f = open(self.employee_date_file, 'w', encoding='gbk')

        else:  # 没有报错，文件报错
            # 读取文件中的数据
            data = f.read()
            if data:
                lst = eval(data)  # 把文件中的字符串，当成python表达式解析
                for dict1 in lst:
                    self.employee_list.append(
                        Employee(dict1['name'], dict1['gender'], dict1['age'], dict1['mobile_number'],
                                 dict1['is_leave']))
        finally:
            if f:
                f.close()


if __name__ == '__main__':
    s = EmployeeManagerSystem()
    s.main()
