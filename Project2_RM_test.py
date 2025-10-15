#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: Project2_RM_test.py
Author: Rafael Martinez

Description: Unit tests for Project2_RM.py.
    These test cases check to make sure that my convex_hull function/algo works correctly:
    - empty edge case
    - co-linear points
    - check for interior points
    - large coordinates
    - tangent edge case
    
Directions: Ensure that the main script is in the same dir. so the import below works. That is all.
"""

import unittest
from Project2_RM import convex_hull

# Here we are storing all our test cases in one class.
class ConvexHullP2Test(unittest.TestCase):

    def test_empty(self):
        """
        TC: Empty list edge case should return an empty list
        
        Testing this with no points to ensure the function handles this gracefully.
        We initialize a "points" array that works in the context of our test case (empty here).
        "self.assert..." is ensuring that we want the result to remain an empty set when processed.
        """
        
        points = []
        result = convex_hull(points)
        
        self.assertEqual(result, [])

    def test_colinear(self):
        """
        TC: Nearly co-linear points with a small change
        
        Testing algo functionality with points that are almost on the same line to see if it handles it correctly.
        We initialize a "points" array that works in the context of our test case (co-linear points here).
        "self.assert..." is ensuring that we want the result to have five points in our answer (that's how we handle it) and that the return is right.
        """
        
        points = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0000000001), (3.0, 3.0), (4.0, 4.0)]
        result = convex_hull(points)
        
        correct = [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0000000001), (3.0, 3.0), (4.0, 4.0)]
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 5)
        self.assertCountEqual(result, correct)

    def test_interior_points(self):
        """
        TC: A square with points inside should return only the 4 corners.
        
        Interior points shouldn't be part of the convex hull.
        We initialize a "points" array that works in the context of our test case (some interior points here).
        "self.assert..." is ensuring that we want the result to be the four points of a square. That's what our hull should "look like".
        """
        
        points = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0), (5.0, 5.0), (3.0, 3.0), (7.0, 7.0)]
        result = convex_hull(points)
        
        correct = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)]
        
        self.assertEqual(len(result), 4)
        self.assertCountEqual(result, correct)
        
    def test_large_coordinates(self):
        """
        TC: Large coordinate values should be handled correctly and gracefully.
        
        Testing algo stability with large numbers.
        We initialize a "points" array that works in the context of our test case (strange and large numbers here).
        "self.assert..." is ensuring that we want the result to be correct for large numbers we pick to put on a plane and that the return is right.
        """
        
        points = [(12345678900, 98765432100), (12345679900, 98765432100), (12345679400, 98765432966), (12345678900, 98765432600)]
        result = convex_hull(points)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 4)
        self.assertCountEqual(result, points)

    def test_tangents(self):
        """
        TC: Setup that messes with tangents in our algo and the merging.
        
        Attempting to see if we could break the upper_tangent and lower_tangent functions through an edge case.
        We initialize a "points" array that works in the context of our test case (negatives and positives here).
        "self.assert..." is ensuring that we want the result to be 5 points for this hull and that the return is right.
        """
        
        points = [(0.0, 0.0), (2.0, 5.0), (1.0, -3.0), (8.0, 1.0), (10.0, 6.0), (9.0, -2.0)]
        result = convex_hull(points)
        
        correct = [(0.0, 0.0), (1.0, -3.0), (9.0, -2.0), (10.0, 6.0), (2.0, 5.0)]
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 5)
        self.assertCountEqual(result, correct)

if __name__ == "__main__":
    unittest.main()