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

    def minBox(self, *vertices): # Identifica el area minima de encerrado
        vx = []
        vy = []
        for v in vertices:
            vx.append(v.x)
            vy.append(v.y)
        vx.sort()
        vy.sort()
        V1 = V2(vx[0], vy[0])
        V12 = V2(vx[-1], vy[-1])

        return V1, V12

    def barycentric(self, A, B, C, P): # Coordenadas baricentricas
        # X
        CAx = C.x - A.x
        BAx = B.x - A.x
        APx = A.x - P.x
        # Y
        CAy = C.y - A.y
        BAy = B.y - A.y
        APy = A.y - P.y

        v1 = V3(CAx, BAx, APx)
        v2 = V3(CAy, BAy, APy)
        bar = self.cross(v1, v2)

        x = bar[0]
        y = bar[1]
        z = bar[2]
        if abs(z) < 1:
            return -1, -1, -1  
        
        return (
            1 - (x + y) / z, 
            y / z, 
            x / z
        )