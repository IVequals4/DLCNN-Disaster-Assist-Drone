import pandas as pd
import cv2
import numpy as np
import matplotlib.pyplot as plt
from veceq import VectorEquation
import math

class Blob:
    def __init__(self, row, col, radius=10):
        self.starting = (row, col)
        self.adjacent_points = []
        self.perimeter = [self.starting]
        self.bfs_marked = []
        self.find_adjacencies()
        self.nearby_points = []
        self.mid_point = self.findMid(self.perimeter)
        # print(f'mid: {self.mid_point}')
        self.furthest_point = self.furthestPoints()
        # print(self.furthest_point)
        self.nearby_points = self.findNearbyPoints(radius)
        self.furthest_cluster_point = self.findMid(self.nearby_points)
        if self.furthest_cluster_point == self.mid_point:
            self.furthest_cluster_point = self.furthest_point
        # print(self.furthest_cluster_point)
        self.vec = self.findVecEquation(self.mid_point, self.furthest_cluster_point)
        
        # for point in self.furthest_cluster_points:
        #     self.vec.append(self.findVecEquation(self.mid_point, point))
        #     print(f'cluster point: {point}')
                    
    def find_adjacencies(self):
        queue = [self.starting]
        while(len(queue) != 0):
            current = queue.pop(0)
            if self.checkSurrounding(current[0], current[1]):
                self.perimeter.append(current)
                
            if self.checkRight(current[0], current[1]):
                temp = self.getNewPoint(current, 0, 1)
                if not temp in marked:
                    queue.append(temp)
                    marked.add(temp)
                    self.adjacent_points.append(temp)
                    
            if self.checkLeft(current[0], current[1]):
                temp = self.getNewPoint(current, 0, -1)
                if not temp in marked:
                    queue.append(temp)
                    marked.add(temp)
                    self.adjacent_points.append(temp)
                    
            if self.checkUp(current[0], current[1]):
                temp = self.getNewPoint(current, -1, 0)
                if not temp in marked:
                    queue.append(temp)
                    marked.add(temp)
                    self.adjacent_points.append(temp)
                    
            if self.checkDown(current[0], current[1]):
                temp = self.getNewPoint(current, 1, 0)
                if not temp in marked:
                    queue.append(temp)
                    marked.add(temp)
                    self.adjacent_points.append(temp)
                    
            
    def findPath(self, start, end):
        points = []
        current = end
        while(current != start):
            points.append(current)
            current = self.edge_to[current]
        return points
    
    def checkRight(self, row, col):
        if col + 1 >= len(image_np[0]): return False
        if image_np[row][col+1] == 0: return False
    
        return True
    
    def checkLeft(self, row, col):
        if col - 1 < 0: return False
        if image_np[row][col-1] == 0: return False
    
        return True
    
    def checkUp(self, row, col):
        if row - 1 < 0: return False
        if image_np[row-1][col] == 0: return False
    
        return True
    
    def checkDown(self, row, col):
        if row + 1 >= len(image_np[0]): return False
        if image_np[row+1][col] == 0: return False
    
        return True
    
    def checkSurrounding(self, row, col):
        white = 0
        if col + 1 >= len(image_np[0]): return True
        if col - 1 < 0: return True
        if row - 1 < 0: return True
        if row + 1 >= len(image_np[0]): return True
    
        if image_np[row+1][col] == 255: white += 1
        if image_np[row-1][col] == 255: white += 1
        if image_np[row][col+1] == 255: white += 1
        if image_np[row][col-1] == 255: white += 1
    
        if white == 4: return False
    
        return True
    
    def findMid(self, points):
        x = np.array([i[0] for i in points])
        y = np.array([i[1] for i in points])
        # print(x)
        # print(y)
        mid_x = 0
        mid_y = 0
        if len(x) > 0:
            mid_x = sum(x) / len(x)
        if len(x) > 0:
            mid_y = sum(y) / len(x)
        return (int(mid_x), int(mid_y))
    
    def furthestPoints(self):
        max_dist = 0
        max_coords = self.mid_point
        for per in self.perimeter:
            temp = self.distance(self.mid_point, per)
            if temp > max_dist:
                max_dist = temp
                max_coords = per
                
        return max_coords
    
    def findNearbyPoints(self, radius):
        within_radius = []
        for point in self.adjacent_points:
            if self.distance(self.furthest_point, point) <= radius:
                within_radius.append(point)
        return within_radius
    
    def findVecEquation(self, p1, p2):
        direction = [p2[1]-p1[1], p2[0]-p1[0]]
        # print(f'direction: {direction}')
        magnitude = self.distance(p1, p2)
        if magnitude <= 0: magnitude = 1
        
        direction[0] = direction[0] / magnitude
        direction[1] = direction[1] / magnitude
        
        return VectorEquation(p1, direction)
    
    def distance(self, p1, p2):
        distance = math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)
        return distance
    
    def getNewPoint(self, p, rowmod, colmod):
        return (p[0] + rowmod, p[1] + colmod);
    
    def getPoints(self):
        return [self.starting] + self.adjacent_points
    
    def inBlob(self, col, row):
        return (col, row) in [self.starting] + self.adjacent_points
    
    def getPerimeter(self):
        return self.perimeter
    
    def getMid(self):
        return self.mid_point
    
    def getFurthestPoint(self):
        return self.furthest_point
    
    def getFurthestClusterpoint(self):
        # print(self.furthest_cluster_points)
        return self.furthest_cluster_point
    
    def getNearbyPoints(self):
        return self.nearby_points


def get_blobs(image):
    # marked = set()
    # blobs = []
    for i in range(img_size[0]):
        for j in range(img_size[0]):
            if image[i][j] != 0 and not (i, j) in marked:
                marked.add((i, j))
                blobs.append(Blob(i, j))
                
    return marked, blobs

def main(mask):
    global image_np
    global marked
    global blobs

    marked = set()
    blobs = []
    
    # _, mask = cv2.threshold(mask,165,255,cv2.THRESH_BINARY)
    # plt.imshow(mask)

    # plt.imshow(mask)
    # plt.savefig(f'mask in main.png')

    image = cv2.resize(mask, img_size, interpolation=cv2.INTER_NEAREST)

    image_np = np.asarray(image)
    # print(image_np)
    df = pd.DataFrame(columns=['x', 'y'])
    index = 0
    for i in range(img_size[0]):
        for j in range(img_size[0]):
            if image_np[i][j] != 0:
                df.loc[index] = (-i, j)
                index += 1

    # plt.imshow(image)

    plt.scatter(df['y'], df['x'])
    plt.axis([0, img_size[0], -img_size[0], 0])
    # plt.show()
    plt.savefig(f'mask after df.png')
    plt.clf()

    marked, blobs = get_blobs(image_np)

    return predict_blockages()
            
    # print(blobs)

def predict_blockages():
    global blocked
    global filename
    blocked = False
    # global image_index

    # Points that intersect the blobs
    hits_p = []

    for blob in blobs:
        # Stores which blobs collide with the vector equation
        hits = []

        # Draws perimeter around blob
        blob_list = blob.getPerimeter()

        # Swap with this one for whole blobs
        # blob_list = blob.getPoints()

        x = np.array([i[0] for i in blob_list])
        y = np.array([i[1] for i in blob_list])
        x = x * -1
        
        # Draws blob
        plt.scatter(y, x, color='blue')

        # Gets mid point of blob
        mid = blob.getMid()

        # Gets the furthest point from the mid point
        furth = blob.getFurthestPoint()
        
        # Gets the adjusted furthest point from the mid point
        # furthc = blob.getFurthestClusterpoint()

        # Travels positively across the vector equation
        i = 1
        coords = blob.vec.calcPosition(i)
        c_x = [coords[0]]
        c_y = [coords[1]]
        while (0 <= coords[0] <= img_size[0] and 0 <= coords[1] <= img_size[0]):
            coords = blob.vec.calcPosition(i)
            c_x.append(coords[0])
            c_y.append(coords[1])
            i += 1

        # Travels negatively across the vector equation
        i = 0
        coords = blob.vec.calcPosition(i)
        while (0 <= coords[0] <= img_size[0] and 0 <= coords[1] <= img_size[0]):
            coords = blob.vec.calcPosition(i)
            c_x.append(coords[0])
            c_y.append(coords[1])
            i -= 1

        # Draws the whole line generated by the vector
        c_x = np.array(c_x)
        c_y = np.array(c_y)
        plt.scatter(c_y, -c_x, color='red')

        # Draws the mid point
        plt.scatter(mid[1], -mid[0])
        
        # For each point on the line, check to see if its inside any blob
        for i in range(len(c_x)):
            for blob_ in blobs:
                if blob_.inBlob(round(c_x[i]), round(c_y[i])):
                    # Store point 
                    hits_p.append((c_x[i], c_y[i]))
        
        
        # CHECKER FOR COLLISIONS FOR ALL OTHER BLOBS
        for blob_ in blobs:
            if blob_ == blob:
                hits.append(blob_)
                continue
            for point in blob_.getPoints():
                if blob.vec.checkPoint(point[1], point[0]):
                    hits.append(blob_)
                    hits_p.append(point)
                    break
                        
        if len(hits) > 1:
            blocked = True
            print(f'blockage at {blob}')
        
        # Draws the region based off of the furthest point
        # nearby = blob.getNearbyPoints()
        # n_x = np.array([i[0] for i in nearby])
        # n_y = np.array([i[1] for i in nearby])
        # n_x = n_x * -1
        
        # plt.scatter(n_y, n_x, color='green')

        # Draws mid point
        plt.scatter(mid[1], -mid[0], color='orange')

        # plt.scatter(furth[1], -furth[0], color='red')
        # plt.scatter(furthc[1], -furthc[0], color='red')
        
    # Draws intersecting points
    for point in hits_p:
        # print(point)
        plt.scatter(point[1], -point[0], color='purple')
        
    plt.axis([0, img_size[0], -img_size[0], 0])
    plt.savefig(f'{filename} vector prediction.png') 
    plt.clf()
    # image_index += 1  

    return blocked

class BlockageAlgorithm:
    def __init__(self, size=(128, 128)):
        global img_size
        img_size=size
        # global image_index
        # image_index = 0 

    def input_from_file(self, filepath):
        mask = cv2.imread(filepath)
        return main(mask)

    def input_from_mask(self, mask, fname):
        global filename
        filename = fname
        # mask = mask.squeeze()
        return main(mask)

if __name__ == '__main__':

    # global marked
    # global blobs
    global img_size

    # marked = set()
    # blobs = []
    img_size=(128, 128)

    # global image_index
    # image_index = 0

    # mask = cv2.imread('/Users/iv/Documents/bingbong/dlcnn/as3/custom dataset/clear/SegmentationClass/165.png', cv2.IMREAD_GRAYSCALE)
    # main(mask)

    # mask = cv2.imread('/Users/iv/Documents/bingbong/dlcnn/as3/custom dataset/blocked2/SegmentationClass/315.png', cv2.IMREAD_GRAYSCALE)
    # main(mask)

    # mask = cv2.imread('/Users/iv/Documents/bingbong/dlcnn/as3/custom dataset/clear/SegmentationClass/99.png', cv2.IMREAD_GRAYSCALE)
    # main(mask)
    # plt.imshow(mask)

    
    # plt.imshow(image)

    
                


                
    