######################################################################
# This file copyright the Georgia Institute of Technology
#
# Permission is given to students to use or modify this file (only)
# to work on their assignments.
#
# You may NOT publish this file or make it available to others not in
# the course.
#
######################################################################

######################################################################
# How to use:
#
#   For fill-in questions, change the value of each answer variable.
#
#   For programming questions, change the implementation of the
#   function provided.
#
#   Run the file from the command line to check:
#
#       python ps1_answers.py
#
######################################################################

import checkutil
import numpy as np
# NOTE: All questions are presented in the problem set videos (lesson modules), please watch these to get the full
# context on the questions below.  Following each question video is a subsequent video with the answer.

# If you see different scores locally and on Gradescope this may be an indication
# that you are uploading a different file than the one you are executing locally.
# If this local ID doesn't match the ID on Gradescope then you uploaded a different file.
OUTPUT_UNIQUE_FILE_ID = False
if OUTPUT_UNIQUE_FILE_ID:
    import hashlib, pathlib
    file_hash = hashlib.md5(pathlib.Path(__file__).read_bytes()).hexdigest()
    print(f'Unique file ID: {file_hash}')

# STUDENT ID

# Please specify your GT login ID in the whoami variable (ex: jsmith223).

whoami = 'jmartinez342'

# QUESTION 1: PROBABILITY

# Question 1, part A
#
# Given:
#
#   P(X) = 0.2
#
# What is P(~X) ?

q1a_P_not_X = 0.8

# Question 1, part B
#
# Given:
#
#   P(X) = 0.2
#   P(Y) = 0.2
#   X,Y independent
#
# What is P(X,Y)?

q1b_P_X_and_Y = 0.04

# Question 1, part C

# Given:
#
#   P(X) = 0.2
#   P(Y|X) = 0.6
#   P(Y|~X) = 0.6
#
# What is P(Y)?

q1c_P_Y = 0.6

# QUESTION 2: LOCALIZATION

# Consider a robot in two-dimensional space whose position is
# specified by (x, y, theta), where x and y are the robot's location
# and theta is the direction the robot is facing.  These variables are
# so-called *state variables*, in that they capture the robot's
# current state.

# In three-dimensional space, we could represent a robot's position
# using (x, y, z, roll, pitch, yaw).  Note that the number of state
# variables has increased from three to six.

# Recall that a *histogram filter* represents the possible states of
# the robot by dividing each dimension of the state space into a fixed
# set of buckets.

# When we use a histogram filter, how does the memory required scale
# in the number of state variables?

possible_answers = ('linearly',
                    'quadratically',
                    'exponentially',
                    'none of the above')

q2_answer = 'exponentially'

# QUESTION 3: BAYES' RULE

# As a hypothetical scenario, say that you live in a house which you
# are worried is likely to catch fire.

# Every day while you are out, you call your neighbor to ask them
# whether your house is on fire.

# Your neighbor always responds with a yes or no, but sometimes they
# lie, saying that your house is on fire when it is not, or vice
# versa.

# Define random variables to represent the events:

#   F := your house is actually on fire
#   B := your neighbor says your house is on fire
#   L := your neighbor lies

# Assume that:

#   P(F) = 0.001
#   P(L) = 0.1

# These values are provided in code below; you may use them in your
# answer if you wish:

q3_P_F = 0.001
q3_P_L = 0.1

# Assume that L is independent of F, that is, your neighbor is equally
# likely to lie whether or not your house is on fire.

# First, compute the non-normalized probability distribution that your
# house is (or is not) on fire given that your neighbor says it is:

#   P`(F|B)
#   P`(~F|B)

# These values will be *proportional* to the true probability
# distribution, but not the same.

# NOTE: Copy/paste using the answer in the video may fail on this one.
# Calculate your answer exactly (without rounding at any step).
# Then round the final answer to 4 decimal places.
# This means the 5th decimal place may influence the result of
# the rounding of the 4th decimal place.

q3_nonnormalized_P_F_given_B     = 0.0009
q3_nonnormalized_P_not_F_given_B = 0.0999

# Next, normalize this distribution such that they form a valid
# probability distribution (hint: in a valid distribution, all the
# probabilities sum to ...?).

#   P(F|B)
#   P(~F|B)

q3_normalized_P_F_given_B        = 0.0089
q3_normalized_P_not_F_given_B    = 0.9911

# QUESTION 4: LOCALIZATION PROGRAM

# The localize function takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up
def sense(p, Z, world, pZ):
    """Variables:
    p: positional probability distribution
    Z: measurment introduced
    world: map of the world
    pZ: probability that measurement is correct"""

    Zv = world == Z
    nonZv = world != Z
    Zprob = Zv*pZ
    nonZprob = nonZv*(1-pZ)
    totProb = Zprob + nonZprob
    q = p*totProb
    sumq = np.sum(q)
    norm_p = q/sumq
    return norm_p

def move(p,U, pExact):
    """Variables:
    p: positional probability distribution
    U: move vector
    pExact: probability that it performs movement"""

    rows, cols = p.shape
    all = np.zeros((rows, cols))
    for row in range(rows):
        for col in range(cols):

            newp = np.zeros((rows, cols)) #initialize probability vector
            index_row = (row + U[0]) % rows
            index_col = (col + U[1]) % cols

            #Calculate new positional indexes, taking into account cyclical world
            newp[index_row, index_col] = pExact*p[row,col]
            newp[row,col] += (1-pExact)*p[row,col]
            all = np.add(all,newp)

    return all



def q4_localize(colors, measurements, motions, sensor_right, p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for _col in range(len(colors[0]))] for _row in range(len(colors))]
    p = np.array(p)
    colors = np.array(colors)
    motions = np.array(motions)
    p_move = np.array(p_move)


    for idx, x in enumerate(measurements):
        p = move(p,motions[idx], p_move)
        p = sense(p, x, colors, sensor_right)

    return p

######################################################################
# Grading methods
#
# Do not modify code below this point.
#
######################################################################

FILL_IN_TEST_CASES = ( { 'variable_name': 'q1a_P_not_X',
                         'str_func':          checkutil.float_to_str,
                         'answer_hash':       'cb3bf9cff573cf1023a496db48717873',
                         'points_avail':      1 },
                       { 'variable_name': 'q1b_P_X_and_Y',
                         'str_func':          checkutil.float_to_str,
                         'answer_hash':       '1721e6da223a39cbdefc6d2a4ac890b5',
                         'points_avail':      1 },
                       { 'variable_name': 'q1c_P_Y',
                         'str_func':          checkutil.float_to_str,
                         'answer_hash':       '90cdc825a24c9cbc7c9ad85cf6f44eff',
                         'points_avail':      1 },
                       { 'variable_name': 'q2_answer',
                         'str_func':          checkutil.do_nothing,
                         'answer_hash':       '35fc100831aa382370331af3161bb254',
                         'points_avail':      1 },
                       { 'variable_name': 'q3_nonnormalized_P_not_F_given_B',
                         'str_func':          checkutil.float_to_str,
                         'answer_hash':       'b0ad2428ec143c68e1c1fc0af6e2de7b',
                         'points_avail':      1 },
                       { 'variable_name': 'q3_nonnormalized_P_F_given_B',
                         'str_func':          checkutil.float_to_str,
                         'answer_hash':       'fd0f9bcd8d7dcf5e24702a74d9faad42',
                         'points_avail':      1 },
                       { 'variable_name': 'q3_normalized_P_not_F_given_B',
                         'str_func':          checkutil.float_to_str,
                         'answer_hash':       'fb07b096e5183434a9409d65857ce150',
                         'points_avail':      1 },
                       { 'variable_name': 'q3_normalized_P_F_given_B',
                         'str_func':          checkutil.float_to_str,
                         'answer_hash':       '3de6c77b2f949cacb49aa53d9938f179',
                         'points_avail':      1 } )

CODE_TEST_CASES = ( { 'function_name': 'q4_localize',
                      'function_input': dict( colors = [['R','G','G','R','R'],
                                                        ['R','R','G','R','R'],
                                                        ['R','R','G','G','R'],
                                                        ['R','R','R','R','R']],
                                              measurements = ['G','G','G','G','G'],
                                              motions = [[0,0],
                                                         [0,1],
                                                         [1,0],
                                                         [1,0],
                                                         [0,1]],
                                              sensor_right = 0.7,
                                              p_move = 0.8, ),
                      'expected_output': [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
                                          [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
                                          [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
                                          [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]],
                      'outputs_match_func': checkutil.arrays_approx_equal,
                      'output_to_str_func': checkutil.format_2d_arr,
                      'points_avail': 8}, )

if __name__ == '__main__':
    checkutil.check(FILL_IN_TEST_CASES, CODE_TEST_CASES, locals())
