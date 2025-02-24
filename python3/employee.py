# "员工类"
class Employee(object):
    # is_leave=0表示在职，1表示离职
    def __init__(self, name, gender, age, mobile_number, is_leave=0):
        self.name = name
        self.gender = gender
        self.age = age
        self.mobile_number = mobile_number
        self.is_leave = False if is_leave == 0 else True  # is_leave=true表示离职，否则就是在职

    def __str__(self):
        msg = '离职' if self.is_leave else '在职'
        return f'{self.name}\t{self.gender}\t{self.age}\t{self.mobile_number}\t{msg}'


if __name__ == "__main__":
    name1 = input('请输入员工的姓名：')
    gender1 = input('请输入员工的性别：')
    age1 = int(input('请输入员工的年龄：'))
    mobile_number1 = input('请输入员工的手机号码：')
    is_leave1 = int(input('请输入员工是否离职，1表示离职，0表示在职：'))
    e = Employee(name1, gender1, age1, mobile_number1, is_leave1)
    print(e.__dict__)
    print(e)
