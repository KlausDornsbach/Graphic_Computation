import window_viewport
import tkinter as tk
from tkinter import ttk
import objects
import transformations
import copy
import obj_converter

# janela principal
class App(tk.Frame):
    def __init__(self):
        super().__init__()
        # instanciamos lista de transformacoes
        self.transformations = []
        # definimos viewport e window
        self.viewport = window_viewport.Viewport(self.master, 600, 400)
        self.window = window_viewport.Window(self.viewport.xVmin - float(self.viewport.xVmax/2),
            self.viewport.yVmin - float(self.viewport.yVmax/2), 
            self.viewport.xVmax - float(self.viewport.xVmax/2), 
            self.viewport.yVmax - float(self.viewport.yVmax/2), 
            self.viewport)
        # inicializa GUI
        self.obj_converter = obj_converter.DescritorOBJ() 
        self.initUI()
        self.object_file = 'obj_src/sample.obj'

    def initUI(self):
        self.master.title('window com viewport')

        # viewport é o canvas, adiciono ao GUI
        self.viewport.grid(column=2, padx=3, pady=1)

        # retas cartesianas
        ponto1 = objects.Ponto(-10000, 0)
        ponto2 = objects.Ponto(10000, 0)
        ponto3 = objects.Ponto(0, -10000)
        ponto4 = objects.Ponto(0, 10000)
        reta1 = objects.Wireframe([ponto1, ponto2], 'x', 'reta', 'red')
        reta2 = objects.Wireframe([ponto3, ponto4], 'y', 'reta', 'blue')

        self.window.objetos.append(reta1)
        self.window.objetos.append(reta2)

        self.window.createObjectNormalized(reta1)
        self.window.createObjectNormalized(reta2)
        # TENHO DE normalizar retas ^

        reta1.drawObjectNormalized(self.window)
        reta2.drawObjectNormalized(self.window)

        under_canvas_frame = tk.LabelFrame(self.master, height=100)
        under_canvas_frame.grid(row=1, column=2)
        under_canvas_frame.grid_propagate
        tk.Label(under_canvas_frame, text='', width=74, height=5).grid(row=0,column=0) # só pra preencher
        # menu elements
        # container menu
        menu_frame = tk.LabelFrame(self.master, text='Menu Options')
        menu_frame.grid(row=0, column=0)

        # objects container
        objects_frame = tk.LabelFrame(menu_frame, text='Objects')
        objects_frame.grid(row=0, column=0, sticky=tk.W, pady=2)

        button_add_object = tk.Button(objects_frame, text='add new object', command=self.windowAddObject)
        button_add_object.grid(row=0, column=0, pady=2)

        list_objects = tk.Listbox(objects_frame, width=15, height=5)
        list_objects.grid(row=1, column=0, pady=2)
        self.list_objects = list_objects

        # object transformations
        button_choose_transformations = tk.Button(objects_frame, text='choose\ntransformation', 
                                            command=self.windowChooseTransformation, height=2)
        button_choose_transformations.grid(row=2, column=0, padx=2, pady=2)

        # + 2 pois tem 2 retas no inicio da lista self.window.objetos
        button_apply_transformations = tk.Button(objects_frame, text='apply\ntransformation', 
            command=lambda:transformations.transform(self.window.objetos[list_objects.curselection()[0]+2],
            self.transformations, self.window), height=2)
        button_apply_transformations.grid(row=3, column=0, padx=2, pady=2)

        # container window
        window_frame = tk.LabelFrame(menu_frame, text='Window')
        window_frame.grid(row=1, column=0, sticky=tk.W, pady=2)

        # step declaration
        step_porcentage = tk.Entry(window_frame, width=4)
        step_porcentage.insert(0, '5')

        # move buttons
        button_up = tk.Button(window_frame, text='^', command=lambda: 
            self.window.moveWindow('up', float(step_porcentage.get())))
        button_up.grid(row=0, column=0, pady=2, columnspan=2)

        button_left = tk.Button(window_frame, text='<', command=lambda: 
            self.window.moveWindow('left', float(step_porcentage.get())))
        button_left.grid(row=1, column=0, pady=2)

        button_right = tk.Button(window_frame, text='>', command=lambda: 
            self.window.moveWindow('right', float(step_porcentage.get())))
        button_right.grid(row=1, column=1, pady=2)

        button_down = tk.Button(window_frame, text='v', command=lambda: 
            self.window.moveWindow('down', float(step_porcentage.get())))
        button_down.grid(row=2, column=0, pady=2, columnspan=2)

        # rotate buttons
        rotate_frame = tk.LabelFrame(menu_frame, text='Rotation')
        rotate_frame.grid(row=2, column=0)

        rotation_parameter = tk.Entry(rotate_frame, width=4)
        rotation_parameter.insert(0, '45')
        rotation_parameter.grid(row=0, column=1, pady=2, padx=4)

        button_left = tk.Button(rotate_frame, text='rotate\nwindow', command=lambda: 
            self.window.rotate(float(rotation_parameter.get())), height=2)
        button_left.grid(row=0, column=0, pady=2, padx=2)
        
        label_deg = tk.Label(rotate_frame, text='°').grid(row=0, column=2, padx=1, pady=2)


        # step put on grid
        step_porcentage.grid(row=0, column=3, padx=5, pady=5)
        label_z = tk.Label(window_frame, text='%').grid(row=0, column=4, padx=0, pady=0)

        button_in = tk.Button(window_frame, text='in', command=lambda: self.window.zoom('in', float(step_porcentage.get())))
        button_in.grid(row=1, column=3, pady=2, columnspan=2)

        button_out = tk.Button(window_frame, text='out', command=lambda: self.window.zoom('out', float(step_porcentage.get())))
        button_out.grid(row=2, column=3, pady=2, columnspan=2)

        # file container
        file_frame = tk.LabelFrame(self.master, text='File')
        file_frame.grid(row=1, column=0)

        button_export = tk.Button(file_frame, text='export', command=lambda: self.toFile(list_objects, 
                                                                    list_objects.curselection()[0]+2))
        button_export.grid(row=4, column=0, padx=2, pady=2)

        button_import = tk.Button(file_frame, text='import', command=lambda: self.fromFile(list_objects))
        button_import.grid(row=5, column=0, padx=2, pady=2)

        button_choose_file = tk.Button(file_frame, text='choose file', command=lambda: self.windowChooseFile())
        button_choose_file.grid(row=6, column=0, padx=2, pady=2)

        # choose clipping button
        button_choose_clipping = tk.Button(self.master, text='choose clipping', command=self.windowChooseClipping())
        button_choose_clipping.grid(row=2, column=0, padx=2, pady=2)

        
    def windowAddObject(self):
        # instantiate popup
        newWindow = tk.Toplevel(self)
        newWindow.title("Create New Object")
        newWindow.geometry("600x400+50+10")
        # name
        tk.Label(newWindow, text ="nome:").grid(row=0, column=0)
        nome = tk.Entry(newWindow, width=20)
        nome.grid(row=0, column=1, pady = 5, padx = 20)
        # color
        tk.Label(newWindow, text ="cor (inglês):").grid(row=1, column=0)
        cor = tk.Entry(newWindow, width=20)
        cor.delete(0, tk.END)
        cor.insert(0, 'black')
        cor.grid(row=1, column=1, pady = 5, padx = 20)
        # tabs menu
        tab_menu = ttk.Notebook(newWindow, width=580)
        tab_ponto = ttk.Frame(tab_menu)
        tab_reta = ttk.Frame(tab_menu)
        tab_wireframe = ttk.Frame(tab_menu)
        tab_curva = ttk.Frame(tab_menu)
        # define abas
        tab_menu.add(tab_ponto, text='Ponto')
        tab_menu.add(tab_reta, text='Reta')
        tab_menu.add(tab_wireframe, text='Wireframe')
        tab_menu.add(tab_curva, text='Curva')

        tab_menu.grid(row=2, columnspan=4, pady = 20, padx=10)
        # instancio frame pra colocar coordenadas dos pontos em cada tab
        ponto_1 = self.label_frame_define_ponto(tab_ponto, 'coordenadas ponto', 0)
        ponto_alt = self.label_frame_define_ponto_alternativo(tab_ponto, 'OU (via texto):', 1, 'Ponto')
        reta_1 = self.label_frame_define_ponto(tab_reta, 'coordenadas ponto 1', 0)
        reta_2 = self.label_frame_define_ponto(tab_reta, 'coordenadas ponto 2', 1)
        reta_alt = self.label_frame_define_ponto_alternativo(tab_reta, 'OU (via texto):', 2, 'Pontos')
        wireframe_1 = self.label_frame_define_ponto(tab_wireframe, 'coordenadas ponto', 0)
        wireframe_alt = self.label_frame_define_ponto_alternativo(tab_wireframe, 'OU (via texto):', 3, 'Pontos')

        # botão OK ponto
        button_ok_ponto = tk.Button(tab_ponto, text="OK", command=lambda: self.window.addObject(
            [self.window.newPonto(ponto_1[1][0].get(), ponto_1[1][1].get())], 
            self.list_objects, nome.get(), cor.get(), newWindow))
        button_ok_ponto.grid(row=0, column=6, padx=10, pady=30)
        # botão OK ponto (alternativo)
        button_ok_ponto_alt = tk.Button(tab_ponto, text="OK", command=lambda: self.window.addObject(
                [self.window.newPonto(self.extractCoordinatesFromText(ponto_alt[1].get())[0][0], 
                self.extractCoordinatesFromText(ponto_alt[1].get())[0][1])], 
                self.list_objects, nome.get(), cor.get(), newWindow))
        button_ok_ponto_alt.grid(row=1, column=6, padx=10, pady=30)
        # botão OK reta
        button_ok_reta = tk.Button(tab_reta, text="OK", command=lambda: self.window.addObject(
                [self.window.newPonto(reta_1[1][0].get(), reta_1[1][1].get()), 
                self.window.newPonto(reta_2[1][0].get(), reta_2[1][1].get())], 
                self.list_objects, nome.get(), cor.get(), newWindow))
        button_ok_reta.grid(row=1, column=6, padx=30, pady=30)
        # botão OK reta (alternativo)
        button_ok_reta_alt = tk.Button(tab_reta, text="OK", command=lambda: self.window.addObject([
            self.window.newPonto(
                self.extractCoordinatesFromText(reta_alt[1].get())[0][0],
                self.extractCoordinatesFromText(reta_alt[1].get())[0][1]),
            self.window.newPonto(
                self.extractCoordinatesFromText(reta_alt[1].get())[1][0],
                self.extractCoordinatesFromText(reta_alt[1].get())[1][1])],
            self.list_objects, nome.get(), cor.get(), newWindow))
        button_ok_reta_alt.grid(row=2, column=6, padx=30, pady=30)
        # checkbox fechar wireframe
        fecha = tk.IntVar() # variavel pra saber se é wireframe fechado
        close_wireframe = tk.Checkbutton(tab_wireframe, text='fechar wireframe: ',variable=fecha, onvalue=1, offvalue=0)
        close_wireframe.grid(row=2, column=1, padx=10, pady=10)
        # botão novo ponto wireframe
        lista_pontos_wireframe = []
        button_new_point_wf = tk.Button(tab_wireframe, text="novo ponto", command=lambda: self.window.addPontoWireframe(
            lista_pontos_wireframe, wireframe_1[1][0], wireframe_1[1][1], self.window))
        button_new_point_wf.grid(row=2, column=0, padx=10, pady=10)
        # botao ok wireframe
        button_ok_wireframe = tk.Button(tab_wireframe, text="OK", command=lambda: 
            self.window.addObject(lista_pontos_wireframe, self.list_objects, 
            nome.get(), cor.get(), newWindow, fecha.get()))
        button_ok_wireframe.grid(row=2, column=2, padx=30, pady=30)
        # checkbox fechar wireframe (alternativo)
        fecha_alt = tk.IntVar() # variavel pra saber se é wireframe fechado (alternativo)
        close_wireframe_alt = tk.Checkbutton(tab_wireframe, text='fechar wireframe: ',variable=fecha_alt, onvalue=1, offvalue=0)
        close_wireframe_alt.grid(row=3, column=1, padx=10, pady=10)
        # botao ok wireframe (alternativo)
        button_ok_wireframe_alt = tk.Button(tab_wireframe, text="OK", command=lambda: 
            self.window.addObject(self.extractPointsFromText(wireframe_alt[1].get(), cor.get()), 
            self.list_objects, nome.get(), cor.get(), newWindow, fecha_alt.get()))
        button_ok_wireframe_alt.grid(row=3, column=2, padx=30, pady=30)

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
    
    # metodo pra facilitar instanciação de elementos graficos para definir pontos
    # (entrada alternativa via texto corrido)
    def label_frame_define_ponto_alternativo(self, pai, titulo, linha, label):
        frame_ponto = tk.LabelFrame(pai, text=titulo)
        frame_ponto.grid(pady=15, padx=10, row=linha)

        label_pontos = tk.Label(frame_ponto, text=label).grid(row=0, column=0, padx=5, pady=5)
        entry_pontos = tk.Entry(frame_ponto, width=20)
        entry_pontos.grid(row=0, column=1, padx=5, pady=5)

        return [frame_ponto, entry_pontos]

    def windowChooseTransformation(self):
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
            'translacao', [float(entry_x.get()), float(entry_y.get())], list_transformations, self.transformations))
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
            'rotacao', [v.get(), float(entry_angulo.get()), float(entry_x_arbitrario.get()), float(entry_y_arbitrario.get())], 
            list_transformations, self.transformations))
        button_add_rotacao.grid(row=5, column=0, pady=2)

        # OK 
        button_ok = tk.Button(newWindow, text='OK', command=lambda: newWindow.destroy())
        button_ok.grid(row=2, column=0, padx=2, pady=2)
        # delete transformation
        del_selected = tk.Button(newWindow, text='delete selected', command=lambda: 
            self.deleteSelected(list_transformations, list_transformations.curselection()[0]))
        del_selected.grid(row=2, column=1, padx=2, pady=2)
        # reset transformation
        del_all = tk.Button(newWindow, text='reset', command=lambda: self.resetTransformations(list_transformations))
        del_all.grid(row=2, column=2, padx=2, pady=2)

    def windowChooseFile(self):
        # instantiate popup
        file_window = tk.Toplevel(self)
        file_window.title("choose file to import/export")
        file_window.geometry("300x100+200+200")

        tk.Label(file_window, text='file name (without .obj)').grid(row=0,column=0)
        entry_file_name = tk.Entry(file_window, width=30)
        entry_file_name.grid(row=1, column=0, padx=5, pady=5)
        

    def windowChooseClipping(self):
        # instantiate popup
        clipping_window = tk.Toplevel(self)
        clipping_window.title("choose clipping method")
        clipping_window.geometry("200x100+800+200")

        clipping = {'Cohen-Sutherland' : 0,
                    '-': 1}
        
        v = tk.StringVar(clipping_window, "0")
        radio_button = [0]*3
        for (text, value) in clipping.items():
            radio_button[value] = tk.Radiobutton(clipping_window, text = text, variable=v,
                value = value).grid(row = value, column = 0, columnspan=2, ipady = 5)

        button_ok = tk.Button(clipping_window, text='OK', command=lambda: self.window.chooseClipping(v.get(), clipping_window))
        button_ok.grid(row=2, column=0, padx=2, pady=2)

    ########################################################
    ## fim das telas, implementacao de funcoes pra janela ##
    ########################################################

    def extractCoordinatesFromText(self, text):
        # text vem no formato '(x,y),(z,w)'
        coordenadas_etapa_1 = text[1:-1] # fica 'x,y),(z,w'
        coordenadas_etapa_2 = coordenadas_etapa_1.split('),(') # fica ['x,y', 'z,w']

        coordenadas_finais = []
        for p in coordenadas_etapa_2:
            x_y = p.split(',') # fica ['x','y']
            coordenadas_finais.append(x_y)

        return coordenadas_finais

    def extractPointsFromText(self, text, cor):
        # '(x,y),(z,w)'
        pontos_etapa_1 = text[1:-1] # fica 'x,y),(z,w'
        pontos_etapa_2 = pontos_etapa_1.split('),(') # fica ['x,y', 'z,w']

        pontos_finais = []
        try:
            for p in pontos_etapa_2:
                x_y = p.split(',') # fica ['x','y']
                x = float(x_y[0])
                y = float(x_y[1])

                p = objects.Ponto(x, y)

                pontos_finais.append(p)

            return pontos_finais
        except ValueError:
            print("NaN")
    
    def addTransformation(self, transform, specs, gui_list, transform_list):
        transform_list.append([transform, specs])
        gui_list.insert(tk.END, transform)
    
    def resetTransformations(self, gui_list):
        self.transformations = []
        gui_list.delete(0, tk.END)

    def deleteSelected(self, gui_list, index):
        self.transformations.pop(index)
        gui_list.delete(index)
    
    def toFile(self, list_objects_gui_component_index): # export
        try:
            self.obj_converter.wireframeToFile(self.object_file, self.window.object_file, list_objects_gui_component_index)
        except FileNotFoundError:
            print("file not found :/")
            print(self.object_file)


    def fromFile(self, list_objects_gui_component): # import
        try:
            self.obj_converter.fileToWireframe(self.object_file, self.window, list_objects_gui_component)
        except FileNotFoundError:
            print("file not found :/")
            print(self.object_file)

    def changeFile(self, file):
        if file == '':
            return
        self.object_file = 'src/' + file + '.obj'

