import window_viewport
import tkinter as tk
from tkinter import ttk
import objects
import transformations

# janela principal
class App(tk.Frame):
    def __init__(self):
        super().__init__()
        # instanciamos lista de transformacoes
        self.transformations = []
        # definimos viewport e window
        self.viewport = window_viewport.Viewport(self.master, 600, 400)
        self.window = window_viewport.Window(self.viewport.xVmin - int(self.viewport.xVmax/2), self.viewport.yVmin - int(self.viewport.yVmax/2), 
            self.viewport.xVmax - int(self.viewport.xVmax/2), self.viewport.yVmax - int(self.viewport.yVmax/2), self.viewport)
        # inicializa GUI
        self.initUI()

    def initUI(self):
        self.master.title('window com viewport')

        # viewport é o canvas, adiciono ao GUI
        self.viewport.grid(rowspan=7, column=2, padx=3, pady=1)

        # retas cartesianas
        ponto1 = objects.Ponto(-2000, 0, self.window)
        ponto2 = objects.Ponto(2000, 0, self.window)
        ponto3 = objects.Ponto(0, -2000, self.window)
        ponto4 = objects.Ponto(0, 2000, self.window)
        reta1 = objects.Object([ponto1, ponto2], 'x', 'reta', 'red')
        reta2 = objects.Object([ponto3, ponto4], 'y', 'reta', 'blue')

        self.window.objetos.append(reta1)
        self.window.objetos.append(reta2)

        self.viewport.create_line(ponto1.xV, ponto1.yV, ponto2.xV, ponto2.yV, fill='red')
        self.viewport.create_line(ponto3.xV, ponto3.yV, ponto4.xV, ponto4.yV, fill='blue')

        under_canvas_frame = tk.LabelFrame(self.master, height=100)
        under_canvas_frame.grid(row=7, column=2)
        under_canvas_frame.grid_propagate
        tk.Label(under_canvas_frame, text='', width=74, height=5).grid(row=0,column=0) # só pra preencher
        # menu elements
        # container menu
        menu_frame = tk.LabelFrame(self.master, text='Menu Options')
        menu_frame.grid(row=0, column=0)

        # objects container
        objects_frame = tk.LabelFrame(menu_frame, text='Objects')
        objects_frame.grid(row=0, column=0, sticky=tk.W, pady=2)

        button_add_object = tk.Button(objects_frame, text='add new object', command=self.addObjectFrame)
        button_add_object.grid(row=0, column=0, pady=2)

        list_objects = tk.Listbox(objects_frame, width=15, height=5)
        list_objects.grid(row=1, column=0, pady=2)
        self.list_objects = list_objects

        # object transformations
        button_choose_transformations = tk.Button(objects_frame, text='choose\ntransformation', command=self.chooseTransformation, height=2)
        button_choose_transformations.grid(row=2, column=0, padx=2, pady=2)

        # + 2 pois tem 2 retas no inicio da lista self.window.objetos
        button_apply_transformations = tk.Button(objects_frame, text='apply\ntransformation', command=lambda:
            transformations.transform(self.window.objetos[list_objects.curselection()[0]+2], self.transformations, self.window, self.viewport), height=2)
        #button_apply_transformations = tk.Button(objects_frame, text='apply\ntransformation', command=lambda: print(self.window.objetos[list_objects.curselection()[0]+2]))
        button_apply_transformations.grid(row=3, column=0, padx=2, pady=2)

        # container window
        window_frame = tk.LabelFrame(menu_frame, text='Window')
        window_frame.grid(row=1, column=0, sticky=tk.W, pady=2)

        # step declaration
        step_porcentage = tk.Entry(window_frame, width=2)
        step_porcentage.insert(0, '5')

        # move buttons
        button_up = tk.Button(window_frame, text='^', command=lambda: self.window.moveWindow('up', int(step_porcentage.get())))
        button_up.grid(row=0, column=0, pady=2, columnspan=2)

        button_left = tk.Button(window_frame, text='<', command=lambda: self.window.moveWindow('left', int(step_porcentage.get())))
        button_left.grid(row=1, column=0, pady=2)

        button_right = tk.Button(window_frame, text='>', command=lambda: self.window.moveWindow('right', int(step_porcentage.get())))
        button_right.grid(row=1, column=1, pady=2)

        button_down = tk.Button(window_frame, text='v', command=lambda: self.window.moveWindow('down', int(step_porcentage.get())))
        button_down.grid(row=2, column=0, pady=2, columnspan=2)

        # step put on grid
        step_porcentage.grid(row=0, column=3, padx=5, pady=5)
        label_z = tk.Label(window_frame, text='%').grid(row=0, column=4, padx=0, pady=0)

        button_in = tk.Button(window_frame, text='in', command=lambda: self.window.zoom('in', int(step_porcentage.get())))
        button_in.grid(row=1, column=3, pady=2, columnspan=2)

        button_out = tk.Button(window_frame, text='out', command=lambda: self.window.zoom('out', int(step_porcentage.get())))
        button_out.grid(row=2, column=3, pady=2, columnspan=2)
        
    def addObjectFrame(self):
        # instantiate popup
        newWindow = tk.Toplevel(self)
        newWindow.title("Create New Object")
        newWindow.geometry("300x400+50+10")
        # name
        tk.Label(newWindow, text ="nome:").grid(row=0, column=0)
        nome = tk.Entry(newWindow, width=20)
        nome.grid(row=0, column=1, pady = 5, padx = 20)
        # tabs menu
        tab_menu = ttk.Notebook(newWindow)
        tab_ponto = ttk.Frame(tab_menu)
        tab_reta = ttk.Frame(tab_menu)
        tab_wireframe = ttk.Frame(tab_menu)
        tab_curva = ttk.Frame(tab_menu)
        # instancio frame pra colocar coordenadas dos pontos em cada tab
        ponto_1 = self.label_frame_define_ponto(tab_ponto, 'coordenadas ponto', 0)
        reta_1 = self.label_frame_define_ponto(tab_reta, 'coordenadas ponto 1', 0)
        reta_2 = self.label_frame_define_ponto(tab_reta, 'coordenadas ponto 2', 1)
        wireframe_1 = self.label_frame_define_ponto(tab_wireframe, 'coordenadas ponto', 0)

        # botão OK ponto
        button_ok_ponto = tk.Button(tab_ponto, text="OK", command=lambda: self.addObject([self.newPonto(ponto_1[1][0].get(), ponto_1[1][1].get())]
                                                                                , "ponto", self.list_objects, nome.get(), newWindow))
        button_ok_ponto.grid(row=2, column=0, padx=30, pady=30)
        # botão OK reta
        button_ok_reta = tk.Button(tab_reta, text="OK", command=lambda: self.addObject([self.newPonto(reta_1[1][0].get(), reta_1[1][1].get()), self.newPonto(reta_2[1][0].get(), reta_2[1][1].get())]
                                                                                , "reta", self.list_objects, nome.get(), newWindow))
        button_ok_reta.grid(row=2, column=0, padx=30, pady=30)
        # checkbox fechar wireframe
        fecha = tk.IntVar() # variavel pra saber se é wireframe fechado
        close_wireframe = tk.Checkbutton(tab_wireframe, text='fechar wireframe: ',variable=fecha, onvalue=1, offvalue=0)
        close_wireframe.grid(row=2, column=0, padx=10, pady=10)
        # botão novo ponto wireframe
        lista_pontos_wireframe = []
        button_new_point_wf = tk.Button(tab_wireframe, text="novo ponto", command=lambda: self.addPontoWireframe(lista_pontos_wireframe, wireframe_1[1][0], wireframe_1[1][1]))
        button_new_point_wf.grid(row=3, column=0, padx=10, pady=10)
        # botao ok wireframe
        button_ok_wireframe = tk.Button(tab_wireframe, text="OK", command=lambda: self.addWireframe(lista_pontos_wireframe
                                                                        , "wireframe", self.list_objects, nome.get(), newWindow, fecha))
        button_ok_wireframe.grid(row=4, column=0, padx=30, pady=30)
        # define abas
        tab_menu.add(tab_ponto, text='Ponto')
        tab_menu.add(tab_reta, text='Reta')
        tab_menu.add(tab_wireframe, text='Wireframe')
        tab_menu.add(tab_curva, text='Curva')

        tab_menu.grid(row=1, columnspan=2, pady = 20, padx=10)

    # metodo pra facilitar instanciação de elementos graficos para definir pontos
    def label_frame_define_ponto(self, pai, titulo, linha):
        frame_ponto = tk.LabelFrame(pai, text=titulo)
        frame_ponto.grid(pady=15, padx=10, row=linha)

        label_x = tk.Label(frame_ponto, text='x:').grid(row=0, column=0, padx=5, pady=5)
        label_y = tk.Label(frame_ponto, text='y:').grid(row=0, column=2, padx=5, pady=5)
        label_z = tk.Label(frame_ponto, text='z:').grid(row=0, column=4, padx=5, pady=5)
        entry_x = tk.Entry(frame_ponto, width=5)
        entry_x.grid(row=0, column=1, padx=5, pady=5)
        entry_y = tk.Entry(frame_ponto, width=5)
        entry_y.grid(row=0, column=3, padx=5, pady=5)
        entry_z = tk.Entry(frame_ponto, width=5)
        entry_z.grid(row=0, column=5, padx=5, pady=5)

        return [frame_ponto, [entry_x, entry_y, entry_z]]
    
    def chooseTransformation(self):
        # instantiate popup
        newWindow = tk.Toplevel(self)
        newWindow.title("Choose transformation")
        newWindow.geometry("400x500+50+10")
        # transformations frame
        t_frame = tk.LabelFrame(newWindow, text='transformacoes')
        t_frame.grid(row=0, column=0, columnspan=2, rowspan=2)
        # list transformations
        label_transformations = tk.Label(newWindow, text='lista de transformacoes').grid(row=0, column=2, padx=5, pady=5)
        list_transformations = tk.Listbox(newWindow, width=15, height=15)
        for i in self.transformations:
            list_transformations.insert(tk.END, i[0])
        list_transformations.grid(row=1, column=2, padx=5, pady=5)
        ########################
        ### frame translacao ###
        ########################
        translacao_frame = tk.LabelFrame(t_frame, text='translacoes')
        translacao_frame.grid(row=0, column=0, columnspan=2)
        label_x = tk.Label(translacao_frame, text='x:').grid(row=0, column=0, padx=5, pady=5)
        label_y = tk.Label(translacao_frame, text='y:').grid(row=0, column=2, padx=5, pady=5)
        entry_x = tk.Entry(translacao_frame, width=5)
        entry_x.grid(row=0, column=1, padx=5, pady=5)
        entry_y = tk.Entry(translacao_frame, width=5)
        entry_y.grid(row=0, column=3, padx=5, pady=5)
        # add translacao
        button_add_translacao = tk.Button(translacao_frame, text='add', command=lambda: self.addTransformation(
            'translacao', [int(entry_x.get()), int(entry_y.get())], list_transformations, self.transformations))
        button_add_translacao.grid(row=1, column=0, pady=2)

        ###########################
        ### frame escalonamento ###
        ###########################
        escalonamento_frame = tk.LabelFrame(t_frame, text='escalonamento')
        escalonamento_frame.grid(row=1, column=0, columnspan=2)
        label_s = tk.Label(escalonamento_frame, text='s:').grid(row=0, column=0, padx=5, pady=5)
        label_useless = tk.Label(escalonamento_frame, width=16).grid(row=0, column=2, columnspan=2, padx=5, pady=5)
        entry_s = tk.Entry(escalonamento_frame, width=5)
        entry_s.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        # add escalonamento
        button_add_translacao = tk.Button(escalonamento_frame, text='add', command=lambda: self.addTransformation(
            'escalonamento', [float(entry_s.get())], list_transformations, self.transformations))
        button_add_translacao.grid(row=1, column=0, pady=2)

        #####################
        ### frame rotacao ###
        #####################
        tipo_rotacao = {'mundo' : 0,
                        'objeto': 1,
                        'arbitrario' : 2}
        rotacao_frame = tk.LabelFrame(t_frame, text='rotacao')
        rotacao_frame.grid(row=2, column=0, columnspan=2)
        v = tk.StringVar(self.master, "1")
        radio_button = [0]*3
        for (text, value) in tipo_rotacao.items():
            radio_button[value] = tk.Radiobutton(rotacao_frame, text = text, variable=v,
                value = value).grid(row = value, column = 0, columnspan=2, ipady = 5)

        label_x_arbitrario = tk.Label(rotacao_frame, text='x:').grid(row=4, column=0, padx=5, pady=5)
        label_y_arbitrario = tk.Label(rotacao_frame, text='y:').grid(row=4, column=2, padx=5, pady=5)
        entry_x_arbitrario = tk.Entry(rotacao_frame, width=5)
        entry_x_arbitrario.grid(row=4, column=1, padx=5, pady=5)
        entry_y_arbitrario = tk.Entry(rotacao_frame, width=5)
        entry_y_arbitrario.grid(row=4, column=3, padx=5, pady=5)
        entry_x_arbitrario.insert(0, '0')
        entry_y_arbitrario.insert(0, '0')

        label_angulo = tk.Label(rotacao_frame, text='angulo:').grid(row=5, columnspan=2, column=1, padx=5, pady=5)
        entry_angulo = tk.Entry(rotacao_frame, width=5)
        entry_angulo.grid(row=5, column=3, padx=5, pady=5)
        # add rotacao
        # if 
        button_add_rotacao = tk.Button(rotacao_frame, text='add', command=lambda: self.addTransformation(
            'rotacao', [v.get(), int(entry_angulo.get()), int(entry_x_arbitrario.get()), int(entry_y_arbitrario.get())], 
            list_transformations, self.transformations))
        button_add_rotacao.grid(row=5, column=0, pady=2)

        # OK 
        button_ok = tk.Button(newWindow, text='OK', command=lambda: newWindow.destroy())
        #button_ok = tk.Button(newWindow, text='OK', command=lambda: print(v.get()))
        button_ok.grid(row=2, column=0, padx=2, pady=2)
        # delete transformation
        del_selected = tk.Button(newWindow, text='delete selected', command=lambda: self.deleteSelected(list_transformations, list_transformations.curselection()[0]))
        del_selected.grid(row=2, column=1, padx=2, pady=2)
        # reset transformation
        del_all = tk.Button(newWindow, text='reset', command=lambda: self.resetTransformations(list_transformations))
        del_all.grid(row=2, column=2, padx=2, pady=2)

    ########################################################
    ## fim das telas, implementacao de funcoes pra janela ##
    ########################################################

    def newPonto(self, x, y):
        try:
            p = objects.Ponto(int(x), int(y), self.window)
            return p
        
        except ValueError:
            print("NaN")
    
    def addPontoWireframe(self, lista, x, y):
        try:
            p = objects.Ponto((int(x.get())), int(y.get()), self.window)
            x.delete(0, tk.END)
            y.delete(0, tk.END)
            lista.append(p)
        except ValueError:
            print("NaN")

    def addObject(self, pontos, tipo_objeto, list_objects_gui_component, nome_gui_component, new_window_gui):
        obj = objects.Object(pontos, nome_gui_component, tipo_objeto)
        self.window.objetos.append(obj)
        nome = nome_gui_component + tipo_objeto
        list_objects_gui_component.insert(tk.END, nome)
        obj.updateAndDrawObject(self.viewport, self.window)
        new_window_gui.destroy()

    def addWireframe(self, pontos, tipo_objeto, list_objects_gui_component, nome_gui_component, new_window_gui, fechado):
        obj = objects.Wireframe(pontos, nome_gui_component, tipo_objeto, fechado)
        self.window.objetos.append(obj)
        nome = nome_gui_component + tipo_objeto
        list_objects_gui_component.insert(tk.END, nome)
        obj.updateAndDrawObject(self.viewport, self.window)
        new_window_gui.destroy()

    def addTransformation(self, transform, specs, gui_list, transform_list):
        transform_list.append([transform, specs])
        gui_list.insert(tk.END, transform)
    
    def resetTransformations(self, gui_list):
        self.transformations = []
        gui_list.delete(0, tk.END)

    def deleteSelected(self, gui_list, index):
        self.transformations.pop(index)
        gui_list.delete(index)

