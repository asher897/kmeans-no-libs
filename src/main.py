# Aaron Sher
# 2568961
# ACML Assignment 2

import math
import random


class DataPoint:
    def __init__(self):
        self.points = []
        self.index: int


class Cluster:
    def __init__(self):
        self.points = []
        self.center = []
        self.cluster_size: int = 0
        self.index: int

    def compute_center(self):
        if not self.points:
            return
        center_mean: float = 0.0
        for i in range(self.cluster_size):
            for point in self.points:
                center_mean += point.points[i]
            center_mean /= len(self.points)
            self.center[i] = center_mean
            center_mean = 0.0

    def sum_of_squares_error(self) -> float:
        loss: float = 0.0
        for i in range(self.cluster_size):
            for point in self.points:
                loss += math.pow((self.center[i] - point.points[i]), 2)

        return loss


class KMeansClusterer:
    def __init__(self):
        self.clusters: [] = []
        self.data_points: [] = []
        self.data_size: int = 0
        self.cluster_size: int = 3

    def compute_distance(self, cluster: Cluster, datapoint: DataPoint) -> float:
        total_distance: float = 0.0
        for i in range(self.data_size):
            total_distance += math.pow(cluster.center[i] - datapoint.points[i], 2)

        return total_distance

    def get_cluster_for_datapoint(self, datapoint: DataPoint) -> None:
        min_distance: float = float("inf")
        chosen_cluster: Cluster
        for cluster in self.clusters:
            current_distance: float = self.compute_distance(cluster=cluster, datapoint=datapoint)
            if current_distance < min_distance:
                min_distance = current_distance
                chosen_cluster = cluster

        chosen_cluster.points.append(datapoint)

    def compute_centers(self):
        for cluster in self.clusters:
            cluster.compute_center()

    def clear_clusters(self):
        for cluster in self.clusters:
            cluster.points.clear()

    def set_cluster_centers(self, centers: []):
        for i in range(self.cluster_size):
            new_cluster: Cluster = Cluster()
            new_cluster.index = i+1
            new_cluster.cluster_size = self.data_size
            new_cluster.center = centers[:2]
            del[centers[0:2]]
            self.clusters.append(new_cluster)

    def get_data(self):
        data_points: [] = []
        datapoint: DataPoint
        i: int = 0
        index: int = 0
        with open('data.txt', 'r') as f:
            points = f.read().split(',')
            points = [float(dp) for dp in points]
        while i < len(points):
            datapoint = DataPoint()
            datapoint.points = ([points[i], points[i+1]])
            datapoint.index = index
            i += 2
            index += 1
            data_points.append(datapoint)

        self.data_points = data_points
        self.data_size = len(self.data_points[0].points)

    def sum_of_squares_loss(self) -> float:
        loss: float = 0.0
        for cluster in self.clusters:
            loss += cluster.sum_of_squares_error()

        return loss

    def clustering(self, loss_threshold=0.5, max_tries=10):
        loss = float('inf')
        tries = 0
        while loss > loss_threshold or tries > max_tries:
            self.clear_clusters()
            for datapoint in self.data_points:
                self.get_cluster_for_datapoint(datapoint=datapoint)

            loss = self.sum_of_squares_loss()
            print("%.4f" % loss)
            self.compute_centers()
            tries += 1

        for cluster in self.clusters:
            print(f'Cluster center: {cluster.center}')
            for dp in cluster.points:
                print(dp.points)


def main():
    clusterer: KMeansClusterer = KMeansClusterer()
    centers = []
    for i in range(6):
        center = random.uniform(0, 1)
        centers.append(center)
    clusterer.get_data()
    clusterer.set_cluster_centers(centers)
    clusterer.clustering()


if __name__ == "__main__":
    main()
