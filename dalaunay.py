
def deltri(points:list[tuple[float]])->list[list[tuple[float]]]:
        """
        Executes a delaunay triangulation, returning the triangles that generate a mesh
        ::INPUT:: 
                -Points: List of points to be used in mesh generation
        ::RETURN::
                -Vertex array: List of triangles that form the mesh
        """
        
        # // Normalize point cloud //
        # Find max coords in point cloud
        x_max = x_min = y_max = y_min = 0
        for point in points: #Finds maxs and mins of both directions
                point_x = point[0]
                point_y = point[1]
                if point_x > x_max:  x_max = point_x
                elif point_x < x_min:  x_min = point_x

                if point_y > y_max:  y_max = point_y
                elif point_y < y_min:  y_min = point_y                

        # Determine the scale factor
        size_x = x_max - x_min
        size_y = y_max - y_min
        if size_x > size_y:
                scale_factor = size_x
        else:
                scale_factor = size_y
                
        # Scale all the points by the scale factor
        points = [((point[0] - x_min)/scale_factor, (point[1] - y_min)/scale_factor  ) for point in points]



        # // BIN SORT //
        # Shorts the points so that when each point is inserted is as close as posible to the last one

        n_cuadros = round(len(points)**(1/4)) 
        len_cuadro = 1 / n_cuadros
        bin_list = {}

        # Determine the containg square for each of the points, and give a number to the points
        for point in points:
                # Determine column and row of the containing square
                if point[0] != 1:
                        column = point[0] // len_cuadro + 1
                else: # Arregla que cuando esta pegado al borde se situa en un cuadro no existente
                        column = point[0] // len_cuadro
                if point[1] != 1:        
                        row = point[1] // len_cuadro + 1 
                else: # Arregla que cuando esta pegado al borde se situa en un cuadro no existente
                        row = point[1] // len_cuadro


                # Determine the corresponding number for the square
                if row % 2 != 0: #Si la fila es impar, crece en -> esta dirección
                        cuadro_id = column + (row - 1)*n_cuadros
                else: # Si la fila es par, crece en <- esta dirección
                        cuadro_id = (row)*n_cuadros - (column - 1)

                # Añadir el "cuadro id" al BIN LIST
                bin_list[point] = cuadro_id

        # Order the points following the "bin-list"
        points = sorted(points, key=lambda point: bin_list[point])

        

        # \\ DELAUN \\
        # Generates the mesh

        vertex_array = [] #List that contains the squares with format [(punto1,punto2,punto3), ... ]
        adjacent_array = {} #Dict that stablishes the neighbours of each triange {"triang_1": [[triang_2], ...}

        # \Supertriangulo\
        """ Se crea el supertriangulo que contiene todos los otros puntos """
        puntos_supertriangulo = [(-100, -100), (100, -100), (0,100)]
        points.extend(puntos_supertriangulo)
        vertex_array.append(puntos_supertriangulo)

        # \Insertar puntos\
        """ Se insertan los puntos uno a uno"""
        for point in points[:-3]: # El [:-3] evita que se itere en los puntos del supertirangulo
                # For each point, its added and the triangles modified so that delaunay is mainained
                __point_iteration(point, vertex_array, adjacent_array)


        # \\ Eliminate supertriangle \\
        #Delete the supertriangle vertexs on the "vertex_array"
        temp_vertex_array = vertex_array.copy()
        for triangle in temp_vertex_array:
                for super_t_point in puntos_supertriangulo:
                        if super_t_point in triangle:
                                vertex_array.remove(triangle)
                                break
        
        # \\ Denormalize point cloud \\
        # Returns the points to their normal size
        points = [( point[0]* scale_factor + x_min , point[1]* scale_factor + y_min  ) for point in points]
        vertex_array = [[( vertex[0]* scale_factor + x_min , vertex[1]* scale_factor + y_min  ) for vertex in triangle] for triangle in vertex_array]


        return  vertex_array








def __point_iteration(point:tuple[float,float], vertex_array:list[list[tuple]], adjacent_array:dict[list[tuple],list[list[tuple]]])->None:
        """
        For each point it is:
                -Added
                -Determine the cotaining triangle, and substituted with 3 triangles that have the point as a vertex
                -Check if delaunay is mantained, if not change the necesary triangles
        :: INPUT ::
                -Point: Point to be added
                -Vertex_array: List that contains the squares with format [(punto1,punto2,punto3), ... ]
                -Adjacent_array: Dict that stablishes the neighbours of each triange {"triang_1": [[triang_2], ...}
        ::RETURN::
                None, the lists are automatically updated
        """

        # \\ Determine containing triangle \\

        # Iteration through points to find the triangle
        for triangle in vertex_array:
                
                # With dot product of the "vector to point" x "edge normal", if for the 3 vertex is the same sign 
                # indicates that the point is inside the triangle
                for i in range(len(triangle)):
                        
                        #Find the normal for the edge of the triangle, pointing outwards
                        edge = [triangle[i - 1], triangle[i]]
                        edge_vector = (edge[1][0] - edge[0][0], edge[1][1] - edge[0][1])
                        edge_normal = (edge_vector[1], - edge_vector[0])
                        
                        #Find the vector for one of the edges to the point
                        vertex_to_point = (point[0] - triangle[i][0], point[1] - triangle[i][1])

                        #Dot product cheks the direction if negative indicates that might be inside
                        in_triangle = vertex_to_point[0]*edge_normal[0] + vertex_to_point[1]*edge_normal[1] <= 0
                        if not in_triangle:
                                # if not inside break and check the next triangle
                                break

                else: # Only reached when the for loop is finished without a break
                        break
        old_triangle = triangle.copy()


        # \\ Substitution with 3 new triangles \\

        vertex_array.remove(old_triangle) # Remove containing triangle
        new_triangles = []
        for i in range(len(old_triangle)):
                #Se escoje un orden aleatorio de los puntos
                x1,y1 = point[0], point[1]
                x2,y2 = old_triangle[i][0], old_triangle[i][1]
                x3,y3 = triangle[i - 1][0], old_triangle[i - 1][1]
                
                #Se calcula el determinante, si > 0 significa que es antihorario y no se cambia, si < 0 se cambia
                det = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
        
                if det > 0: 
                        new_triangle = [(x1,y1),(x2,y2),(x3,y3)]
                else:
                        new_triangle = [(x1,y1),(x3,y3),(x2,y2)]

                new_triangles.append(new_triangle)
                vertex_array.insert(0, new_triangle)
        
        # \\ Update "adjacent array" \\
        
        # Se tienen los tres nuevos triangulos en "new_triangles"
        try:
                old_neighbours = adjacent_array[tuple(old_triangle)] # Vecinos del antiguo triangulo
                posible_neighbours = new_triangles + old_neighbours # Contiene todos los triangulos cuyos vecinos se vieron modificados
        except:
                posible_neighbours = new_triangles
        
        # \\ Check that the delaunay is mantained \\
        for triangle in new_triangles: 

                # Se itera en cada triangulo nuevo, buscando sus vecinos entre los "posible neigbours"
                deleted_pos = posible_neighbours.index(triangle)
                posible_neighbours.remove(triangle) # Se elimina al propio triangulo para evitar que se encuentre a si mismo como vecino
                adjacent_array[tuple(triangle)] = [] # Crea la lista para el nuevo triangulo que se acaba de crear.
                for i in range(3):
                        # Se itera a lo largo de los 3 vertices revisando asi las 3 aristas comparandolas con los 
                        # posible neighbours para ver si coinciden.
                        vertex_1 = triangle[i - 1]
                        vertex_2 = triangle[i]
                        for posible_neighbour in posible_neighbours:
                                if vertex_1 not in posible_neighbour or  vertex_2 not in posible_neighbour: # No comparte la arista con el vecino
                                        continue # Buscar en el siguiente posible vecino
                                

                                # Actualizar el nuevo triangulo
                                if vertex_1 == point or vertex_2 == point:
                                        # Si uno de los vertices es el punto añadido, entoces este vecino no es el triangulo opuesto.
                                        adjacent_array[tuple(triangle)].append(posible_neighbour)
                                else:
                                        # Si ningun vertice es el punto, este vecino es el triangulo opuesto.
                                        adjacent_array[tuple(triangle)].insert(0, posible_neighbour)

                                # Actualizar el vecino, para que pase de referenciar al triangulo previo y pase al nuevo triangulo
                                if posible_neighbour not in new_triangles:
                                        i = adjacent_array[tuple(posible_neighbour)].index(old_triangle) # Determinar en que posicion del array se contraba el triangulo antiguo
                                        adjacent_array[tuple(posible_neighbour)][i] = triangle # Se sustituye el antiguo por el nuevo

                                break # Continua con el siguiente arista del triangulo

                        else: # Solo se llega si no encontró un vecino
                                if vertex_1 == point or vertex_2 == point:
                                        # Si uno de los vertices es el punto añadido, entoces este vecino no es el triangulo opuesto.
                                        adjacent_array[tuple(triangle)].append([0])
                                else:
                                        # Si ningun vertice es el punto, este vecino es el triangulo opuesto.       
                                        adjacent_array[tuple(triangle)].insert(0,[0])

                posible_neighbours.insert(deleted_pos,triangle) # Se vuelve a añadir el triangulo que se elimino al principio para evitar que se encuentre a si mismo
        
        try:
                del adjacent_array[tuple(old_triangle)]
        except:
                pass

        
        # \\ APPLY DELAUNAY \\
        stack = new_triangles
        while len(stack) > 0:
                print("__"*50)
                triangle = stack[0]
                opposite_triangle = adjacent_array[tuple(triangle)][0]
                if opposite_triangle == [0]: #If there is no opposite triangle
                        stack.pop(0)
                        continue 
                #Point nomenclature based of paper
                p = point
                v1 = triangle[2]
                v2 = triangle[1]
                for vertex in opposite_triangle:
                        if vertex != v1 and vertex !=v2:
                                v3 = vertex
                
                # Swich the points so that "p" is to the left of the v1-v2 edge for the delaunay conditions
                calc_p = point
                calc_v1 = triangle[2]
                calc_v2 = triangle[1]
                calc_v3 = v3

                side = (p[0] - v2[0])*(v1[1] - v2[1]) - (p[1] - v2[1])*(v1[0]- v2[0])


                if side > 0:
                        temp = calc_p
                        calc_p = calc_v3
                        calc_v3 = temp
                

                
                # Check the delaunay conditions
                x13 = calc_v1[0] - calc_v3[0]
                x23 = calc_v2[0] - calc_v3[0]
                x1p = calc_v1[0] - calc_p[0]
                x2p = calc_v2[0] - calc_p[0]

                y13 = calc_v1[1] - calc_v3[1]
                y23 = calc_v2[1] - calc_v3[1]
                y1p = calc_v1[1] - calc_p[1]
                y2p = calc_v2[1] - calc_p[1]               


                # \ Check if swap is needed \

                cos_a = (x13*x23 + y13*y23)
                cos_b = (x2p*x1p + y2p*y1p)
                sin_a = (x13*y23 - x23*y13)
                sin_b = (x2p*y1p - x1p*y2p)
                sin_ab = sin_a*cos_b + cos_a*sin_b



                if cos_a >= 0 and cos_b >= 0:
                        stack.pop(0)
                        continue # Pasa al siguiente triangulo a comprobar del stack
                elif cos_a < 0 and cos_b < 0:
                        print(1)
                        pass # A swap is needed, becaus this is true the next elif is ignored
                elif sin_ab < 0:
                        pass
                else:
                        stack.pop(0)
                        continue # A swap is needed, becaus this is true the next elif is ignored


                
                # Save the original triangles previous to the change (will be automatically updated if not copied)
                #to be able to check and modify the adjacent array later
                old_triangle = triangle.copy()
                old_opposite_triangle = opposite_triangle.copy()
                # se buscan los triangulos vecinos que cambian para ambos, para realizar el cambio posteriormente
                p_v2_neighbour = v1_v3_neighbour = v2_v3__neigbour = [0]
                for neighbour in adjacent_array[tuple(triangle)]:
                        if p in neighbour and v2 in neighbour:
                                p_v2_neighbour = neighbour
                                break
                for neighbour in adjacent_array[tuple(opposite_triangle)]:
                        if v1 in neighbour and v3 in neighbour:
                                v1_v3_neighbour = neighbour
                        elif v2 in neighbour and v3 in neighbour:
                                v2_v3__neigbour = neighbour
                                

                # \\ Execute swap \\


                # En triangle se cambia V2 por V3 
                triangle[1] = v3
                # En opposite se vambia V1 por P
                opposite_triangle.remove(v1)
                opposite_triangle.insert(0,p)



                # \\ Update "adjacent array" \\

                # Actualizar apara el "triangle"
                new_triangle_adjacents = adjacent_array[tuple(old_triangle)].copy()
                del adjacent_array[tuple(old_triangle)] #Remove old triangle adjacent array
                new_triangle_adjacents.remove(p_v2_neighbour)
                new_triangle_adjacents.insert(0, v1_v3_neighbour) # Pasa a ser el vecino opuesto
                adjacent_array[tuple(triangle)] = new_triangle_adjacents

                # Actualizar para el "opposite-triangle"
                new_opposite_triangle_adjacents = adjacent_array[tuple(old_opposite_triangle)].copy()
                del adjacent_array[tuple(old_opposite_triangle)] #Remove old triangle adjacent array
                # Hacer el cambio entre los vecinos que dejan de ser y el que empieza a ser
                new_opposite_triangle_adjacents.remove(v1_v3_neighbour)
                new_opposite_triangle_adjacents.append(p_v2_neighbour)
                # Eliminar y insertar al principio al triangulo que pasa aser el opposite triangle
                new_opposite_triangle_adjacents.remove(v2_v3__neigbour)
                new_opposite_triangle_adjacents.insert(0, v2_v3__neigbour)
                adjacent_array[tuple(opposite_triangle)] = new_opposite_triangle_adjacents               

                # Actualizar a los vecinos
                if v1_v3_neighbour != [0]:
                        adjacent_array[tuple(v1_v3_neighbour)][adjacent_array[tuple(v1_v3_neighbour)].index(opposite_triangle)] = triangle
                if p_v2_neighbour != [0]:
                        adjacent_array[tuple(p_v2_neighbour)][adjacent_array[tuple(p_v2_neighbour)].index(triangle)] = opposite_triangle
                


                # \\ Delete the current triangle of the stack \\
                stack.pop(0)
                # Because the 2 triangles where swiched they must be checked
                stack.insert(0,triangle)
                stack.insert(1, opposite_triangle)















if __name__ == "__main__":
        import pygame


        def centra_coord(point):
                """Centra el sistema de coordenadas"""
                point_scaled = (point[0]  - 150, point[1]  - 110)
                point_coord = (int(point_scaled[0] + screen_size[0]/2), int(screen_size[1]/2 - point_scaled[1]))
                return point_coord

        def centra_coord_noscale(points:list[tuple,tuple, tuple]):
                new_points =[]
                for point in points:
                        point_coord = (int(point[0] + screen_size[0]/2), int(screen_size[1]/2 - point[1]))
                        new_points.append(point_coord)
                return new_points



        def render_points(points):
                for id, point in enumerate(points):
                        pygame.draw.circle(screen,"white", centra_coord(point), 3)
                        # Mostrar el numero por el que se ordena tras la funcion "BSort" (unicamente para visualización)
                        text = font.render(str(id + 1), 1, "white")
                        screen.blit(text, centra_coord(point))
                        




        def render_cuadros(n_cuadros):
                for x in range(0, n_cuadros + 1):
                        pygame.draw.line(screen, "blue", centra_coord((x/n_cuadros, 0)), centra_coord((x/n_cuadros, 1)))
                for y in range(0, n_cuadros + 1):
                        pygame.draw.line(screen, "blue", centra_coord((0, y/n_cuadros)), centra_coord((1, y/n_cuadros)))



        def render_color_array(vertex_array:list[list[tuple,tuple,tuple]]):
                for i, triangle in enumerate(vertex_array):
                        coords = []
                        for point in triangle:
                                coords.append(centra_coord(point))
                        colors = ["blue", "gray", "white", "purple", "yellow", "red", "orange", "green", "turquoise2", "springgreen1", "royalblue4"]
                        pygame.draw.polygon(screen, colors[i], coords)



        def render_array(vertex_array:list[list[tuple,tuple,tuple]]):
                for triangle in vertex_array:
                        for i in range(len(triangle)):
                                pygame.draw.line(screen, "red", centra_coord(triangle[i-1]), centra_coord(triangle[i]))

        scale_factor = 1


        # points = [(-40,-10),(-60, -40), (30,10), (10,-20),(50, -40), (0, 70), (50,50), (-50, 50), (-20, 30)]
        points = [(-100, -100), (-200,-300), (400, -200), (300, 400), (100, 100), (-200, 300), (-200, 200)]

        # pygame setup
        pygame.init()
        screen_size = (1280, 720)
        screen = pygame.display.set_mode(screen_size)
        clock = pygame.time.Clock()
        running = True
        font = pygame.font.SysFont("calibri", 15, True)





        while running:

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                running = False
        
                        if event.type == pygame.KEYDOWN:
                                vertex_array = deltri(points)

                screen.fill("black")
                try:
                        render_array(vertex_array)
                except:
                        pass



                render_points(points)
                

                pygame.display.flip()
                clock.tick(60)

        pygame.quit()





