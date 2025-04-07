
def deltri(points:list[tuple[float]], constrain_island:list[list[list[tuple[float]]]])->list[list[tuple[float]]]:
        """
        Executes a delaunay triangulation, returning the triangles that generate a mesh
        ::INPUT:: 
                -Points: List of points to be used in mesh generation
                -Constrain Edges: Ilands of of constrain edges, each iland in it's own list.
        ::RETURN::
                -Vertex array: List of triangles that form the mesh
        """
        # \\ Add the contrain edges points to the points \\
        constrain_edges = []
        for island in constrain_island:
                constrain_edges.extend(island)
                


        for edge in constrain_edges:
                for point in edge:
                        if point not in points:
                                points.append(point)




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

        constrain_edges = [[((point[0] - x_min)/scale_factor, (point[1] - y_min)/scale_factor) for point in edges] for edges in constrain_edges]

        constrain_island = [[[((point[0] - x_min)/scale_factor, (point[1] - y_min)/scale_factor) for point in edges] for edges in islands] for islands in  constrain_island  ]




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

        # \\ Insertar puntos \\
        """ Se insertan los puntos uno a uno"""
        for point in points[:-3]: # El [:-3] evita que se itere en los puntos del supertirangulo
                # For each point, its added and the triangles modified so that delaunay is mainained
                __point_iteration(point, vertex_array, adjacent_array)
        




        # \\ CONSTRAIN EDGE \\
        
        # \\ Loop over constrain edges \\
        for edge in constrain_edges:

                # \\ Check if the edge is already in the triangulation \\
                already_present = False
                for triangle in vertex_array:
                        if edge[0] in triangle and edge[1] in triangle:
                                # Edge already present
                                already_present = True
                                break
                if already_present:
                        continue # Go to the next edge


                # \\ Search for intersecting edges \\
                intersecting_edges = []
                # Get the triangles that contains one of the verteces of the constrain edge
                for triangle in vertex_array:
                        if edge[0] not in triangle:
                                continue
                        # If contains the point, find out if the edge intersects the triangle 
                        #(has to be in the edge that doesnt contain the constrain point)
                        edge_vertex_index = triangle.index(edge[0])
                        triangle_edge = (triangle[edge_vertex_index - 1], triangle[edge_vertex_index - 2]) 
                        if edge_intersection(edge, triangle_edge):
                                break # if they intersect break the cicle
                intersecting_edges.append(triangle_edge)

                for i in range(4):
                        # Find the corresponding next triangle
                        #must share the edge crossed by the constrain edge
                        for neighbour in adjacent_array[tuple(triangle)]:
                                if triangle_edge[0] in neighbour and triangle_edge[1] in neighbour:
                                        triangle = neighbour
                                        break


                        if edge[1] in triangle:
                                # if the triangle contains the other constrain vertex the loop is over
                                break

                        for i in range(3):
                                new_triangle_edge = (triangle[i -1], triangle[i])

                                if triangle[i -1] in triangle_edge and triangle[i] in triangle_edge:
                                        # Evita que seleccione la misma arista por la que entró
                                        continue
                                
                                if edge_intersection(edge, new_triangle_edge):
                                        triangle_edge = new_triangle_edge
                                        intersecting_edges.append(triangle_edge)
                                        break
                


                # \\ Loop over intersecting edges \\

                new_edges = []
                while len(intersecting_edges) > 0:
                # for i in range(5):




                        intersect_edge = intersecting_edges[0]


                        # Find the triangles that share the edge
                        for triangle in vertex_array: #Search for 1 of the 2 triangles
                                if intersect_edge[0] in triangle and intersect_edge[1] in triangle:
                                        triangle_1 = triangle
                                        break

                        for triangle in adjacent_array[tuple(triangle_1)]: # Use the 1º triangle to find the 2º faster
                                if intersect_edge[0] in triangle and intersect_edge[1] in triangle:
                                        triangle_2 = triangle
                                        break
                        


                        # Define the cuadrilateral formed by the triangles
                        
                        # Determine the 2 points that are not in the intersecting edge
                        cuadrilateral =  []
                        cuadrilateral.extend(triangle_1)
                        cuadrilateral.extend(triangle_2)
                        cuadrilateral = list(set(cuadrilateral)) #Removes the duplicates
                        cuadrilateral.remove(intersect_edge[0])
                        cuadrilateral.remove(intersect_edge[1])
                        cuadrilateral.insert(0, intersect_edge[0])
                        cuadrilateral.insert(2, intersect_edge[1])

                        # Determine if quadrilateral convex, if it's not convex continue to the next triangle
                        previous_vector_product = 0
                        convex = True
                        for i in range(4):
                                # Loop over the 4 sides, calculating the vectorial product by pairs
                                #if the sing is different between them is not convex
                                side_1 = (cuadrilateral[i-2], cuadrilateral[i-1])
                                side_2 = (cuadrilateral[i-1], cuadrilateral[i])
                                vector_side_1 = (side_1[1][0] - side_1[0][0], side_1[1][1] - side_1[0][1])
                                vector_side_2 = (side_2[1][0] - side_2[0][0], side_2[1][1] - side_2[0][1])

                                vector_product = vector_side_1[0]*vector_side_2[1] - vector_side_1[1]*vector_side_2[0]
                                if vector_product * previous_vector_product < 0: # if sign is different to the prevous end the loop
                                        convex = False
                                        break
                                previous_vector_product = vector_product        
                        
                        if not convex:
                                # Remove the edge and place it at the end
                                intersecting_edges.append(intersect_edge)
                                intersecting_edges.pop(0)
                                continue

                        # This part is executed if the cuadrilateral is convex

                        # Swap the diagonal

                        p  = cuadrilateral[3]
                        v1 = cuadrilateral[0]
                        v2 = cuadrilateral[2]
                        v3 = cuadrilateral[1]

                        if v2[1] > v1[1]:
                                temp = v2
                                v2 = v1
                                v1 = temp


                        side = (p[0] - v2[0])*(v1[1] - v2[1]) - (p[1] - v2[1])*(v1[0]- v2[0])


                        if side > 0:
                                temp = p
                                p = v3
                                v3 = temp
                        
                        if p not in triangle_1:
                                temp = triangle_1
                                triangle_1 = triangle_2
                                triangle_2 = temp




                        triangle_swap(triangle_1, triangle_2, adjacent_array, p, v1, v2, v3)







                        intersecting_edges.remove(intersect_edge) # remove the constrain edge
                        intersect_edge = (p,v3)
                        # If the new edge intersects the constrain edge, add-it to the list again
                        
                        print((intersect_edge), (edge))
                        if edge_intersection(intersect_edge, edge):
                                print("Edge added")
                                #If the new edge still intersects add it again
                                intersecting_edges.append(intersect_edge)
                        else:
                                # If the new edge doesnt intersect save it
                                for edge in constrain_edges:
                                        if edge == intersect_edge:
                                                break
                                        if edge[0] == intersect_edge[1] and edge[1] == intersect_edge[0]:
                                                break
                                else:
                                        new_edges.append((intersect_edge))


                
                # \\ Ensure that delaunay is mantained \\
                while len(new_edges) > 0:
                        print("__"*20)
                        edge = new_edges[0]
                        print(edge_tetx(edge))

                        # \check that the edge is not a constrain edge
                        if edge in constrain_edges:
                                new_edges.pop(0)

                        # Find the triangles that share the edge
                        for triangle in vertex_array: #Search for 1 of the 2 triangles
                                if edge[0] in triangle and edge[1] in triangle:
                                        triangle_1 = triangle
                                        break

                        for triangle in adjacent_array[tuple(triangle_1)]: # Use the 1º triangle to find the 2º faster
                                if edge[0] in triangle and edge[1] in triangle:
                                        triangle_2 = triangle
                                        break

                        print(triang_text(triangle_1))
                        print(triang_text(triangle_2))


                        if triangle_2 == [0]: #If there is no opposite triangle
                                new_edges.pop(0)
                                continue 
                        #Point nomenclature based of paper
                        v1 = edge[0]
                        v2 = edge[1]
                        for vertex in triangle_2:
                                if vertex != v1 and vertex !=v2:
                                        v3 = vertex
                        for vertex in triangle_1:
                                if vertex != v1 and vertex !=v2:
                                        p = vertex
                        
                        print(point_text(p), point_text(v1), point_text(v2), point_text(v3))
                        
                        # Swich the points so that "p" is to the left of the v1-v2 edge for the delaunay conditions
                        calc_p = p
                        calc_v3 = v3
                        if v1[1] > v2[1]:
                                calc_v1 = v2 
                                calc_v2 = v1
                        else:
                                calc_v1 = v1
                                calc_v2 = v2

                        side = (p[0] - v2[0])*(v1[1] - v2[1]) - (p[1] - v2[1])*(v1[0]- v2[0])


                        if side > 0:
                                temp = calc_p
                                calc_p = calc_v3
                                calc_v3 = temp
                        

                        print(point_text(calc_p), point_text(calc_v1), point_text(calc_v2), point_text(calc_v3))
                        
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
                                new_edges.pop(0)
                                continue # Pasa al siguiente triangulo a comprobar del stack
                        elif cos_a < 0 and cos_b < 0:
                                pass # A swap is needed, becaus this is true the next elif is ignored
                        elif sin_ab < 0:
                                pass
                        else:
                                new_edges.pop(0)
                                continue # A swap is needed, becaus this is true the next elif is ignored


                        
                        print("swap")
                        triangle_swap(triangle_1, triangle_2, adjacent_array, p, v1, v2, v3)
                        


                        # \\ Delete the current triangle of the stack \\
                        new_edges.pop(0)

        for i in adjacent_array:
                a = f"{triang_text(i)}||\t"
                for t in adjacent_array[tuple(i)]:
                        if t!=[0]:
                                a += triang_text(t) + "|  "

                print(a)



        # \\ Mantain or eliminate triangles in the islands \\
        # Each island should form a closed polygon:
        #   -Check that is an island
        #   -Identify all the triangles on the outline of the polygon
        #   -Identify all the triangles inside the polygon
        for island in constrain_island:
                # \Check that is an island
                
                # The first and last point must be the same
                if island[0][0] != island[-1][-1]:
                        break

                # \\ Identify all the triangles on the outline of the polygon  
                for edge in island:
                        pass




         

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


        return  vertex_array, points








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

        # Iterate through the triangles to find the containing one
        for triangle in vertex_array:
                
                # The dot product of "vector to point" x "edge normal" for each edge, if all are the same sign its inside the triangle
                for i in range(3):
                        
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
        # The old triangle is substituted for 3 new triangles with the added point as a vertex
        #       -Remove the old triangle
        #       -For the 3 new triangles:
        #               -Select 3 points, the first is the added point and 2 others from the old triangle
        #               -Check that the order of the points is in counter-clock, starting from the new point
        #                       -If it's not, swap the position of the 2º and third triangles

        vertex_array.remove(old_triangle) # Remove containing triangle
        new_triangles = [] # used to update the adjacent array

        for i in range(3): # For the 3 triangles
                # Select 3 points, the first is the added point and 2 others from the old triangle
                x1,y1 = point[0], point[1]
                x2,y2 = old_triangle[i][0], old_triangle[i][1]
                x3,y3 = old_triangle[i - 1][0], old_triangle[i - 1][1]
                
                # Check the order of the points, if the determinant is positive is counterclockwise and no need tho change
                det = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
        
                if det > 0: 
                        new_triangle = [(x1,y1),(x2,y2),(x3,y3)]
                else: # swap the position of the 2º and third triangles to make it counter clock
                        new_triangle = [(x1,y1),(x3,y3),(x2,y2)]

                new_triangles.append(new_triangle)
                vertex_array.insert(0, new_triangle)
        




        # # \\ Update "adjacent array" \\
        # To mantain the adjacent array updated after the triangle changes.
        #       -Generate a list of posible neighbours
        #       -For each triangle check that delaunay is mantained        
        #               -Find each of their neighbours
        #               -Add it to the adjacent array
        #               -If it's an old triangle neighbour change it so that it references the new triangle
        # 


        
        # \ Generate a list of posible neigbours
        # The triangles affected are the 3 new triangles and the old triangle neighbours
        try:
                old_neighbours = adjacent_array[tuple(old_triangle)] 
                posible_neighbours = new_triangles + old_neighbours 
        except:
                posible_neighbours = new_triangles
        

        # \\ Check that the delaunay is mantained \\
        for triangle in new_triangles: 
                # Delete the own triangle to avoid finding itself as a neighbour
                deleted_pos = posible_neighbours.index(triangle)
                posible_neighbours.remove(triangle) 


                adjacent_array[tuple(triangle)] = []
                # Iterate through the 3 edges
                for i in range(3):
                        vertex_1 = triangle[i]
                        if i == 2:
                                vertex_2 = triangle[0]
                        else:
                                vertex_2 = triangle[i + 1]

                        # Compare the edge to the possible neighbours
                        for posible_neighbour in posible_neighbours:
                                if vertex_1 not in posible_neighbour or  vertex_2 not in posible_neighbour: 
                                        # Doesnt match, search the next possible neighbour
                                        continue 
                                
                                # The possible neighbour shares the edge, add it to the triangle's adjacent array
                                adjacent_array[tuple(triangle)].append(posible_neighbour)


                                # If its an old triangle neighbour update it's vertex array
                                if posible_neighbour not in new_triangles:
                                        i = adjacent_array[tuple(posible_neighbour)].index(old_triangle) # Determinar en que posicion del array se contraba el triangulo antiguo
                                        adjacent_array[tuple(posible_neighbour)][i] = triangle # Se sustituye el antiguo por el nuevo

                                print(adjacent_array)

                                break # Continua con la siguiente arista del triangulo

                        else: # Solo se llega si no encontró un vecino
                                        adjacent_array[tuple(triangle)].append([0])


                posible_neighbours.insert(deleted_pos,triangle) # Se vuelve a añadir el triangulo que se elimino al principio para evitar que se encuentre a si mismo
        
        try:
                del adjacent_array[tuple(old_triangle)]
        except:
                pass

        
        # \\ APPLY DELAUNAY \\
        stack = new_triangles
        while len(stack) > 0:
                triangle = stack[0]
                opposite_triangle = adjacent_array[tuple(triangle)][1]
                if opposite_triangle == [0]: #If there is no opposite triangle
                        stack.pop(0)
                        continue 
                #Point nomenclature based of paper
                p = triangle[0]
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
                        pass # A swap is needed, becaus this is true the next elif is ignored
                elif sin_ab < 0:
                        pass
                else:
                        stack.pop(0)
                        continue # A swap is needed, becaus this is true the next elif is ignored


                


                triangle_swap(triangle, opposite_triangle, adjacent_array, p, v1, v2, v3)
                


                # \\ Delete the current triangle of the stack \\
                stack.pop(0)
                # Because the 2 triangles where swiched they must be checked
                stack.insert(0,triangle)
                stack.insert(1, opposite_triangle)





def edge_intersection(edge_1:list[tuple[float]], edge_2:list[tuple[float]]) -> bool:
        """
        Checks if 2 edges intersect
        ::INPUT::
                -edge_1: edge defined by 2 vertex
                -edge_2: edge defined by 2 vertex
        ::OUTPUT::
                -True: they intersect
                -False: they dont intersect
        """
        # \\ Sort the edges to garantee that go form left to right
        edge_1 = list(edge_1)
        edge_1.sort(key=lambda x: x[0])
        edge_2 = list(edge_2)
        edge_2.sort(key=lambda x: x[0])

        # \\ Get the line equations \\
        m1 = (edge_1[1][1] - edge_1[0][1]) / (edge_1[1][0] - edge_1[0][0])
        c1 = edge_1[0][1] - m1 * edge_1[0][0]
        m2 = (edge_2[1][1] - edge_2[0][1]) / (edge_2[1][0] - edge_2[0][0])
        c2 = edge_2[0][1] - m2 * edge_2[0][0]

        # \\ Get the intersecction point \\
        if m1 == m2: # Paralell
                return False

        x_intersection = round((c2 - c1) / (m1 - m2), 5)

        if edge_1[0][0] < x_intersection < edge_1[1][0] and edge_2[0][0] < x_intersection < edge_2[1][0]:
                return True
        else:
                return False






def triangle_swap(triangle:list, opposite_triangle, adjacent_array, p , v1, v2, v3):
        """
        Executes the triangle swap between a triangle pair and auto-updates the neighbours.
        ::INPUT::
                -Triangle: triangle 1.
                -oppossite-triangle: triangle 2.
                -Adjacent_array: list that contains the triangles neighbours.
                -P, v1, v2, v3: points following the nomenclature of the S.W. Sloan paper.
        """




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
        triangle[triangle.index(v2)] = v3
        # En opposite se vambia V1 por P (el resto de cambios es para mantener el sentido anti-horario, comenzando en P)
        opposite_triangle.remove(v1)
        opposite_triangle.remove(v3)
        opposite_triangle.insert(0,p)
        opposite_triangle.append(v3)



        # \\ Update "adjacent array" \\

        # Actualizar apara el "triangle"
        new_triangle_adjacents = adjacent_array[tuple(old_triangle)].copy()
        del adjacent_array[tuple(old_triangle)] #Remove old triangle adjacent array
        new_triangle_adjacents.remove(p_v2_neighbour)
        new_triangle_adjacents.insert(1, v1_v3_neighbour) # Insertado en la 2º posición para mantener el sentido anti-horario
        adjacent_array[tuple(triangle)] = new_triangle_adjacents

        # Actualizar para el "opposite-triangle"
        new_opposite_triangle_adjacents = adjacent_array[tuple(old_opposite_triangle)].copy()
        del adjacent_array[tuple(old_opposite_triangle)] #Remove old triangle adjacent array
        # Hacer el cambio entre los vecinos que dejan de ser y el que empieza a ser
        a = []
        new_opposite_triangle_adjacents.clear()
        # Eliminar y insertar al principio al triangulo que pasa aser el opposite triangle
        new_opposite_triangle_adjacents.append(p_v2_neighbour)
        new_opposite_triangle_adjacents.append(v2_v3__neigbour)
        new_opposite_triangle_adjacents.append(triangle)
        
        adjacent_array[tuple(opposite_triangle)] = new_opposite_triangle_adjacents               

        # Actualizar a los vecinos
        if v1_v3_neighbour != [0]:
                adjacent_array[tuple(v1_v3_neighbour)][adjacent_array[tuple(v1_v3_neighbour)].index(opposite_triangle)] = triangle
        if p_v2_neighbour != [0]:
                adjacent_array[tuple(p_v2_neighbour)][adjacent_array[tuple(p_v2_neighbour)].index(triangle)] = opposite_triangle
                








if __name__ == "__main__":
        import pygame

        def triang_text(triangle):
                res = ""
                for point in triangle:
                        res += f"{point_text(point)}; "
                return res

        def edge_tetx(edge):
                res = ""
                for point in edge:
                        res += f"{point_text(point)}; "
                return res

        def point_text(point):
                points = [(0.0, 0.0), (0.2, 0.2), (0.8, 0.2), (0.8, 0.0), (0.0, 1.0), (0.2, 1.0), (-100, -100), (100, -100), (0, 100)]
                return str (points.index(point) + 1)



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





        # points = [(-40,-10),(-60, -40), (30, 10), (10,-20),(50, -40), (0, 70), (50, 50), (-50, 50), (-20, 30)]
        # constrain_edge = [[(50, 50), (-50 , 50)], [(50, 50), (10, -20)]]
        # points = [(-100, -100), (-200,-300), (400, -200), (300, 400), (100, 100), (-200, 300), (-200, 200)]

        points = [(0,0), (0,100), (20,100), (20,20), (80,20), (80,0)]
        constrain_edge = [[[(0,0), (0,100)], [(0,100), (20,100)], [(20,100), (20,20)], [(20,20), (80,20)], [(80,20), (80,0)], [(80,0), (0,0)]]]

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
                                vertex_array, points = deltri(points, constrain_edge)

                screen.fill("black")
                try:
                        render_array(vertex_array)
                except:
                        pass



                render_points(points)
                

                pygame.display.flip()
                clock.tick(60)

        pygame.quit()





