import flet as ft
import sqlite3


def create_table() -> None:
    conn = sqlite3.connect(database="student.db", check_same_thread=False)
    cur = conn.cursor()
    cur.execute("""
        create table if not exists student(
            id integer primary key autoincrement,
            name varchar(25),   
            email varchar(50),
            phone varchar(25),   
            address varchar(25),
            francais decimal,   
            arabic decimal,   
            maths decimal,   
            chime decimal,   
            design decimal,   
            english decimal   
        )  
    """)
    conn.commit()
    cur.close()
    conn.close()


create_table()


def get_data() -> list[tuple]:
    con = sqlite3.connect("student.db")
    cur = con.cursor()
    cur.execute("select * from student"),
    data = cur.fetchall()
    return data


def get_sum(data: list[tuple], i: int) -> int | float:
    for j in data:
        if j[0] == i+1:
            return sum(j[5:])
    else:
        return 0


class Dialog(ft.AlertDialog):
    def __init__(self, ee: sqlite3.Error) -> None:
        super().__init__()

        self.modal = True
        self.title = ft.Text(value="WARNING !", color="#DE6751")
        self.content = ft.Text(value=str(ee))
        self.actions = [
            ft.TextButton("Yes", on_click=self.handle_close),
            ft.TextButton("No", on_click=self.handle_close),
        ]

    def handle_close(self, e: ft.ControlEvent):
        e.page.close(self)


class SelectStudent(ft.View):

    def __init__(self) -> None:
        super().__init__(
            route="/select", scroll=ft.ScrollMode.HIDDEN, padding=ft.padding.only(left=20, right=20, bottom=20, top=30)
        )

        self.controls = [
            ft.Container(
                alignment=ft.alignment.center,
                bgcolor="#57B1FD",
                border_radius=ft.border_radius.all(value=25),
                padding=ft.padding.all(value=10),
                content=self.card(i),
            )
            for i in range(len(get_data()))
        ]
        self.controls.append(
            Main.button("Add Student", width=360, on_click=lambda e: e.page.go("/"))
        )
        self.controls.insert(0, self.__text(
            value="Students", size=25, color="#DE6751", weight=ft.FontWeight.BOLD
        ))

    @staticmethod
    def __text(value: str, span: str | int | float = None, size: int = 14,  **kwargs) -> ft.Text:
        return ft.Text(
            value=value, size=size,
            spans=[
                ft.TextSpan(
                    text=span,
                    style=ft.TextStyle(color=ft.colors.WHITE)
                )
            ],
            **kwargs
        )

    @staticmethod
    def __text_result(adm) -> ft.Text:
        if adm > 50:
            return ft.Text(
                value="Result Final: ",
                weight=ft.FontWeight.BOLD,
                spans=[
                    ft.TextSpan(
                        style=ft.TextStyle(color="#DE6751"),
                        text=f"   {adm}",
                    ),
                    ft.TextSpan(
                        text="   Acceptable   🥰",
                    )
                ]
            )
        else:
            return ft.Text(
                value="Result Final: ",
                weight=ft.FontWeight.BOLD,
                spans=[
                    ft.TextSpan(
                        style=ft.TextStyle(color="#DE6751"),
                        text=f"   {adm}",
                    ),
                    ft.TextSpan(
                        text="   unacceptable   😭",
                    )
                ]
            )

    def card(self, i: int) -> ft.Column:
        data = get_data()
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(name=ft.icons.PERSON),
                        ft.Column(
                            controls=[
                                self.__text(value=f"Name: {data[i][1]}",
                                            weight=ft.FontWeight.BOLD),
                                self.__text(value=f"Student Email: {data[i][2]}",
                                            weight=ft.FontWeight.BOLD),
                            ]
                        )
                    ]
                ),
                ft.Row(
                    controls=[
                        self.__text("-Phone Number: ", f"{data[i][3]}"),
                        self.__text("-Address: ", f"{data[i][4]}"),
                    ]
                ),
                ft.Row(
                    controls=[
                        self.__text("-Maths: ", f"{data[i][5]}"),
                        self.__text("-Arabic: ", f"{data[i][6]}"),
                        self.__text("-Francais: ", f"{data[i][7]}"),
                    ]
                ),
                ft.Row(
                    controls=[
                        self.__text("-English: ", f"{data[i][8]}"),
                        self.__text("-Design: ", f"{data[i][9]}"),
                        self.__text("-chime: ", f"{data[i][10]}"),
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.__text_result(get_sum(data, i))
                    ]
                )

            ]
        )


class Main(ft.View):
    def __init__(self):
        super().__init__(
            route="/",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            bgcolor=ft.colors.WHITE,
            padding=ft.padding.only(left=20, right=30, bottom=20, top=30)
        )
        self.image = ft.Image(
            #  src="stud2.jpg",
            #  src="https://th.bing.com/th/id/OIP.lMudmfiiOrnshfgTQ53yoAHaHa?pid=ImgDet&w=192&h=192&c=7",
            src="https://th.bing.com/th/id/OIP.dkCi7_71hy0zKPtJ8ukkigHaGS?pid=ImgDet&w=192&h=162&c=7",
            width=250,
            height=200
        )

        self.controls = [
            self.image,
            ft.Text(
                value="App teacher and student in your pocket".title(),
                weight=ft.FontWeight.BOLD,
                font_family="Calibri"
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        value="number of student registered: ".title(),
                        weight=ft.FontWeight.BOLD,
                        font_family="Calibri",
                        color="#DE6751"
                    ),
                    ft.Text(
                        value=self.num_rows(),
                        weight=ft.FontWeight.BOLD,
                    )
                ]
            ),
            ft.Container(height=10),
            self.text_field(label="Student Name", icon=ft.icons.PERSON),
            self.text_field(label="Email", icon=ft.icons.EMAIL),
            self.text_field(label="Phone Number", icon=ft.icons.PHONE),
            self.text_field(label="Address", icon=ft.icons.HOUSE),
            ft.Text(
                value="Marks Student",
                weight=ft.FontWeight.BOLD,
                size=17
            ),
            ft.Row(
                controls=[
                    self.text_field(label="Francais", width=103),
                    self.text_field(label="Arabic", width=103),
                    self.text_field(label="Maths", width=103)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[
                    self.text_field(label="Chime", width=103),
                    self.text_field(label="Design", width=103),
                    self.text_field(label="English", width=103)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.button(text="Add Student", on_click=self.add_student),
                    self.button(text="Select Student", on_click=self.select_student),
                ]
            )
        ]

    @staticmethod
    def text_field(label: str, icon: str = None, **kwargs) -> ft.TextField:
        return ft.TextField(
            label=label,
            icon=icon,
            height=40,
            cursor_color="#DE6751",
            cursor_height=21,
            **kwargs
        )

    @staticmethod
    def button(text: str, width: int | float = None, **kwargs) -> ft.ElevatedButton:
        return ft.ElevatedButton(
            text=text,
            width=width if width else 160,
            style=ft.ButtonStyle(
                bgcolor="#DE6751",
                color=ft.colors.WHITE,
                padding=ft.padding.all(value=15),
            ),
            **kwargs
        )

    @staticmethod
    def select_student(e: ft.ControlEvent) -> None:
        e.page.go("/select")

    @staticmethod
    def add_student(e: ft.ControlEvent) -> None:
        conn = sqlite3.connect(database="student.db", check_same_thread=False)
        cur = conn.cursor()
        try:
            cur.execute(f"""
                insert into student(
                    name, email, phone, address, francais, arabic, maths,
                    chime, design, english
                    
                ) values( 
                    '{e.control.parent.parent.controls[4].value}', 
                    '{e.control.parent.parent.controls[5].value}', 
                     {e.control.parent.parent.controls[6].value}, 
                    '{e.control.parent.parent.controls[7].value}', 
                     {e.control.parent.parent.controls[9].controls[0].value}, 
                     {e.control.parent.parent.controls[9].controls[1].value}, 
                     {e.control.parent.parent.controls[9].controls[2].value}, 
                     {e.control.parent.parent.controls[10].controls[0].value}, 
                     {e.control.parent.parent.controls[10].controls[1].value}, 
                     {e.control.parent.parent.controls[10].controls[2].value}
                )
            """)
            conn.commit()
        except sqlite3.Error as ee:
            e.page.open(Dialog(ee))
        cur.close()
        conn.close()
        e.control.parent.parent.controls[2].controls[1].value = Main.num_rows()
        e.control.parent.parent.controls[2].controls[1].update()
        Main.clear(e)

    @staticmethod
    def num_rows() -> str:
        conn = sqlite3.connect(database="student.db", check_same_thread=False)
        n: int = conn.execute("select count(*) from student").fetchone()[0]
        conn.close()
        return str(n)

    @staticmethod
    def clear(e: ft.ControlEvent) -> None:
        e.control.parent.parent.controls[4].value = ""
        e.control.parent.parent.controls[5].value = ""
        e.control.parent.parent.controls[6].value = ""
        e.control.parent.parent.controls[7].value = ""
        e.control.parent.parent.controls[9].controls[0].value = ""
        e.control.parent.parent.controls[9].controls[1].value = ""
        e.control.parent.parent.controls[9].controls[2].value = ""
        e.control.parent.parent.controls[10].controls[0].value = ""
        e.control.parent.parent.controls[10].controls[1].value = ""
        e.control.parent.parent.controls[10].controls[2].value = ""
        e.page.update()


def main(page: ft.Page) -> None:
    page.title = "Student Note"
    #  page.window.top = 1
    page.window.height = 740
    page.window.width = 370
    #  page.window.left = 960
    page.theme_mode = ft.ThemeMode.LIGHT

    def router(route: str) -> None:
        page.views.clear()
        match page.route:
            case "/": page.views.append(Main())
            case "/select": page.views.append(SelectStudent())
            case _: page.launch_url("http://www.google.com")
        page.update()

    page.on_route_change = router
    page.go("/")

    page.update()


ft.app(target=main)
