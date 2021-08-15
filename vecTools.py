from collections import namedtuple

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])

class VecTools():

    def sum(self, v1, v2): # Suma de Vectores
        x = v1.x + v2.x
        y = v1.y + v2.y
        z = v1.z + v2.z
        return V3(x, y, z)

    def sub(self, v1, v2): # Resta de Vectores
        x = v1.x - v2.x
        y = v1.y - v2.y
        z = v1.z - v2.z
        return V3(x, y, z)

    def mul(self, v, k): # Multiplicacion Escalar de Vectores
        x = v.x*k
        y = v.y*k
        z = v.z*k
        return V3(x, y, z)

    def dot(self, v1, v2): # Producto Punto
        x = v1.x*v2.x
        y = v1.y*v2.y
        z = v1.z*v2.z
        dot = x + y + z
        return dot

    def cross(self, v1, v2): # Producto Cruz
        x = v1.y * v2.z - v1.z * v2.y
        y = v1.z * v2.x - v1.x * v2.z
        z = v1.x * v2.y - v1.y * v2.x
        return V3(x, y, z)

    def length(self, vector): # Tamano del vector
        x2 = vector.x**2
        y2 = vector.y**2
        z2 = vector.z**2
        lenght = (x2 + y2 + z2)**0.5
        return lenght

    def normal(self, vector): # Calculo de la Normal
        vecLen = self.length(vector)

        if vecLen == 0:
            return V3(0, 0, 0)

        xLen = vector.x/vecLen
        yLen = vector.y/vecLen
        zLen = vector.z/vecLen
        
        return V3(xLen, yLen, zLen)

    def bbox(self, *vertices): # ?????????
        """
            Input: n size 2 vectors
            Output: 2 size 2 vectors defining the smallest bounding rectangle possible
        """  
        xs = [ vertex.x for vertex in vertices ]
        ys = [ vertex.y for vertex in vertices ]
        xs.sort()
        ys.sort()

        return V2(xs[0], ys[0]), V2(xs[-1], ys[-1])

    def barycentric(self, A, B, C, P): # ?????????
        """
            Input: 3 size 2 vectors and a point
            Output: 3 barycentric coordinates of the point in relation to the triangle formed
                    * returns -1, -1, -1 for degenerate triangles
        """  
        cx, cy, cz = self.cross(
            V3(B.x - A.x, C.x - A.x, A.x - P.x), 
            V3(B.y - A.y, C.y - A.y, A.y - P.y)
        )

        if abs(cz) < 1:
            return -1, -1, -1   # this triangle is degenerate, return anything outside

        # [cx cy cz] = [u v 1]

        u = cx/cz
        v = cy/cz
        w = 1 - (u + v)

        return w, v, u