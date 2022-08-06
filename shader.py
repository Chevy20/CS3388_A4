"""
CS 3388 Assignment 4
Name: Matthew Cheverie
Student Number: 251098050

Shader Class:
The purpose of this class is to determine the color of pixels based on the lighting and objects around. It implements
ray tracing to determine shadowing and shading of light
"""


class shader:

    # Constructor
    # Params:
    # Intersection - the first intersection from the intersection list
    # direction - the direction of the ray
    # camera - the camera object
    # objectList - the list of objects in the scene
    # light - the light source
    def __init__(self, intersection, direction, camera, objectList, light):

        # Consider the tuple (k, t0) from intersection param
        index = intersection[0]
        # Get object from object list
        object = objectList[index]

        # t0 is t value from the tuple
        t0 = intersection[1]

        # Compute inverse of the matrix T associated with object
        mInverse = object.getT().inverse()

        # Compute Ts which is the light position transformed with M-1
        Ts = mInverse * light.getPosition()

        # Transform the way in the following way:
        # Te = M-1 * e, where e is position of the camera
        Te = mInverse * camera.getE()

        # Td = M-1 * d, where d is the direction of the ray
        Td = mInverse * direction

        # Compute intersection point
        I = Te + (Td.scalarMultiply(t0))

        # Compute vector from intersection point to light soruce, then normalize
        S = (Ts - I).normalize()

        # Compute normal vector at intersection point
        N = object.normalVector(I)

        # Compute Specular Reflection vector
        R = -S + N.scalarMultiply(((S.scalarMultiply(2)).dotProduct(N)))

        # Compute vector to center of projection, normalize
        V = (Te - I).normalize()

        # Compute Id
        Id = max((N.dotProduct(S)), 0)

        # Compute Is
        Is = max((R.dotProduct(V)), 0)

        # Get reflectance of an object
        r = object.getReflectance()

        # Get color of the object
        c = object.getColor()

        # Get intensity of the light
        Li = light.getIntensity()

        # Determine if the intersection point is shadowed or not by other objects using call to shadowed

        # If shadowed
        if self.__shadowed(object, I, S, objectList):
            # Compute f
            f = r[0]

        # If not Shadowed
        else:
            # Compute f
            f = r[0] + (r[1] * Id) + (r[2] * (Is ** r[3]))

        # Compute Color Tuple
        self.__color = (int(c[0] * Li[0] * f), int(c[1] * Li[1] * f), int(c[2] * Li[2] * f))

    # Shadowed function
    # This function determines if the ray from the intersection point to the light intersects another object from the scene
    # Params:
    # object - the object to determine if there is intersection with
    # I - intersection point
    # S - vector to light source
    # objectList - list of objects
    def __shadowed(self, object, I, S, objectList):

        #Epsilon constant
        EPSILON = 0.001

        # Get T matrix associated with object
        M = object.getT()

        # Detach the intersection point from the surface of the object and transform into world Coords
        I = M * (I + S.scalarMultiply(EPSILON))

        # Transforms S into world coordinates
        S = M * S

        # For each object in the scene
        for obj in objectList:

            # Get inverse of matrix M (T matrix of object parameter)
            mInv = obj.getTinv()

            # Transform intersection point into the generic coordinates of the object param
            I2 = mInv * I

            # Transform the vector to the light soruce into the generic coordinates of the object param
            S2 = (mInv * S).normalize()

            # Determine if there is intersection
            if obj.intersection(I2, S2) != -1.0:
                return True
        return False

    def getShade(self):
        return self.__color
