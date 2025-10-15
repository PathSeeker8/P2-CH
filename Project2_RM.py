#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: Project2_RM.py
Author: Rafael Martinez

Description:
    This script is the divide & conquer recursive algo for computing the convex hull on a set of points. Accomplished in the O(n log n) time asked for while deduping and handling special case logic (bug inspired).

Pseudocode (D&C Convex Hull):
    Preprocessing: Sort the points by x-coordinate
    Divide the set of points into two sets A and B:
        A contains the left ⌊n/2⌋ points
        B contains the right ⌈n/2⌉ points
    Recursively compute the convex hull of A
    Recursively compute the convex hull of B
    Merge the two convex hulls
        
Lines of code (without whitespace/comments):
  - orientation: 1
  - rightmost_point: 10
  - leftmost_point: 10
  - upper_tangent: 14
  - lower_tangent: 14
  - hull_merge: 33
  - convex_hull: 6
  - divide_and_conquer: 23
  - main: 16 (not really part of the algo)
  Total: 111 lines of code for algorithm, + 16 for execution

Time Complexity:
  Overall script runs O(n log n) time, where "n" is the number of input points (points on an x, y axis). Individual method/function runtimes written in the project document.
  Total: O(n log n)
"""

# Importing built-in Python modules for list, tuple, random, csv, and timing related ops
from typing import List, Tuple
import random, time, csv

# Old code, not used
# Point = Tuple[float, float]
# Hull = List[Point]

# This is a geometric primitive method to determine the orientation (shared knowledge, cited in doc)
def orientation(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

# Finds the rightmost point for the tangents, returns the index of the rightmost (and topmost) point.
def rightmost_point(hull):
    if not hull:
        raise ValueError("Hull is empty")
    
    best_index = 0
    best_x, best_y = hull[best_index]
    
    for index in range(1, len(hull)):
        x, y = hull[index]
        if x > best_x or (x == best_x and y > best_y):
            best_index = index
            best_x, best_y = x, y
    return best_index

# Finds the leftmost point for the tangents, returns the index of the leftmost (and bottommost) point.
def leftmost_point(hull):
    if not hull:
        raise ValueError("Hull is empty")
    
    best_index = 0
    best_x, best_y = hull[best_index]
    
    for index in range(1, len(hull)):
        x, y = hull[index]
        if x < best_x or (x == best_x and y < best_y):
            best_index = index
            best_x, best_y = x, y
    return best_index

# Calculates the upper tangent between two convex hulls.
def upper_tangent(left_hull, right_hull):
    left_n = len(left_hull)
    right_n = len(right_hull)
    
    # Start from rightmost point of left hull and leftmost point of right hull
    left_index = rightmost_point(left_hull)
    right_index = leftmost_point(right_hull)
    
    # Adjusts both indexes until we find the upper tangent
    done = False
    
    while not done:
        done = True
        
        # Adjust left index
        while orientation(right_hull[right_index], left_hull[left_index], left_hull[(left_index + 1) % left_n]) < 0:
            left_index = (left_index + 1) % left_n
            done = False
        
        # Adjust right index
        while orientation(left_hull[left_index], right_hull[right_index], right_hull[(right_index - 1 + right_n) % right_n]) > 0:
            right_index = (right_index - 1 + right_n) % right_n
            done = False
    
    return left_index, right_index

# Calculates the lower tangent between two convex hulls.
def lower_tangent(left_hull, right_hull):
    left_n = len(left_hull)
    right_n = len(right_hull)
    
    # Start from rightmost point of left hull and leftmost point of right hull
    left_index = rightmost_point(left_hull)
    right_index = leftmost_point(right_hull)
    
    # Adjusts both indices until we find the lower tangent
    done = False
    
    while not done:
        done = True
        
        # Adjust left index
        while orientation(right_hull[right_index], left_hull[left_index], left_hull[(left_index - 1 + left_n) % left_n]) > 0:
            left_index = (left_index - 1 + left_n) % left_n
            done = False
        
        # Adjust right index
        while orientation(left_hull[left_index], right_hull[right_index], right_hull[(right_index + 1) % right_n]) < 0:
            right_index = (right_index + 1) % right_n
            done = False
    
    return left_index, right_index

# Essentially merges the hulls together into one using the found upper and lower tangents.
def hull_merge(left_hull, right_hull):
    if not left_hull:
        return right_hull
    if not right_hull:
        return left_hull
    
    # Handles strange co-linear case correctly. When all hull points were co-linear, our code was coming back wrong somewhere in the tangents.
    union = left_hull + right_hull
    point_min = min(union)
    point_max = max(union)
    if all(orientation(point_min, point_max, point) == 0 for point in union):
        return [point_min] if point_min == point_max else [point_min, point_max]
    
    # Single point case check for extra safety due to a previous bug.
    if len(left_hull) == 1 and len(right_hull) == 1:
        left_point, right_point = left_hull[0], right_hull[0]
        return [left_point, right_point] if left_point != right_point else [left_point]
    
    # Finds the tangent points
    upper_left_index, upper_right_index = upper_tangent(left_hull, right_hull)
    lower_left_index, lower_right_index = lower_tangent(left_hull, right_hull)
    
    # Makes the merged hull by walking from the upper tangent to the lower on the left hull, then from lower tangent to upper on the right hull, forming a full merged hull. (All lines to "return merged")
    merged = []
    
    # Add upper tangent point from left hull
    merged.append(left_hull[upper_left_index])
    
    # Walk along left hull from upper to lower tangent
    if upper_left_index != lower_left_index:
        index = (upper_left_index + 1) % len(left_hull)
        while index != lower_left_index:
            merged.append(left_hull[index])
            index = (index + 1) % len(left_hull)
        merged.append(left_hull[lower_left_index])
    
    # Add lower tangent point from right hull (if different)
    if left_hull[lower_left_index] != right_hull[lower_right_index]:
        merged.append(right_hull[lower_right_index])
    
    # Walk along right hull from lower to upper tangent
    if lower_right_index != upper_right_index:
        index = (lower_right_index + 1) % len(right_hull)
        while index != upper_right_index:
            merged.append(right_hull[index])
            index = (index + 1) % len(right_hull)
        merged.append(right_hull[upper_right_index])
    
    # Removes dupe points where the hulls meet and check if first and last points are the same.
    if len(merged) > 1 and merged[0] == merged[-1]:
        merged.pop()
    
    return merged

# Main function and direct D&C implementation of Option #5 Convex Hull to get the points.
def convex_hull(points):
    if not points:
        return []
    points = sorted(set(points))    # This is our "n log n" preprocessing/sorting.
    if len(points) == 1:
        return points

    # The nested recursive D&C part that builds the actual convex hull.
    def divide_and_conquer(sorted_points):
        n = len(sorted_points)
        if n <= 3:  # Base handling for n == 3
            if n == 1:
                return sorted_points
            if n == 2:
                return sorted_points
            
            a, b, c = sorted_points
            turn = orientation(a, b, c)
            if turn > 0:
                return [a, b, c]
            elif turn < 0:
                return [a, c, b]
            else:
                return [a, c]

        middle_index = n // 2
        
        # Handles ties when it lands on "x" to ensure a normal median (multiple points with the same "x", etc.), either stays or moves left.
        mid_x = sorted_points[middle_index][0]
        while middle_index > 0 and sorted_points[middle_index - 1][0] == mid_x:
            middle_index -= 1
        if middle_index == 0:
            middle_index = n // 2
        
        # Here is where our D&C happens.
        left_hull = divide_and_conquer(sorted_points[:middle_index])
        right_hull = divide_and_conquer(sorted_points[middle_index:])
        return hull_merge(left_hull, right_hull)

    return divide_and_conquer(points)

# Execution logic and where we do our tests for the values of "n". Put here to save runtime (in case).
if __name__ == "__main__":
    
    random.seed(31) # Using a seed lets us reproduce the points, in case.

    # Choose the "n" value amounts here
    n_values = [100, 500, 1000, 5000, 10000, 50000, 100000, 500000]

    # Range for our int coordinate points
    Min_Coordinate, Max_Coordinate = 0, 5000

    print(f"\nRunning Convex Hull test...on point range: [{Min_Coordinate}, {Max_Coordinate}]\n")
    print("n, nanoseconds")

    with open("results.csv", mode="a", newline="") as file:
        output = csv.writer(file)
        output.writerow(["n", "nanoseconds"])

        # Loop where we generate the "n" random (x, y) pairs
        for n in n_values:
            generated_points = [(random.randint(Min_Coordinate, Max_Coordinate), random.randint(Min_Coordinate, Max_Coordinate)) for i in range(n)]

            start = time.perf_counter_ns()
            convex_hull(generated_points)
            elapsed = time.perf_counter_ns() - start

            print(f"{n}, {elapsed} ns")
            output.writerow([n, elapsed])
    
    print(f"\nResults saved to file.")