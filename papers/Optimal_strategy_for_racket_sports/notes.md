# Intro

We want to find optimal strategy for playing singles in tennis and pickleball.
The methodology is general and can be extended to other games with two opponents

# Problem description

## Approximations and Assumptions

The geometry of the courts are the following
// TODO

Ignore air friction, spin

Assume a maximum speed of ball of xyz

Human reflexes are XYZ

The range of speed of a human moving on the court is XYZ

Ignore the bio mechanics of hitting a shot given one position:
we assume a player is in the ideal position to hit the ball
and what matters is the direction on the angles and strength 
for the ball

We do not simulate 3d but rather approximate the problem with 1d or 2d when
possible to simplify the analysis

## Problem 1: Ideal Position of the Ball

Given the position of the ball on the court and the position of the opponent,
what is the best placement of the next shot (considering distance, travel time,
geometry, distribution of errors, speed of other player)?

## Sub-problem 1: Travel time and forces applied

Given the position of the ball and the opponent player, and the net compute the
needed trajectory and the travel time 
(It can be modeled as 1d problem)

Compute the angle and the force to hit the ball to get that trajectory

## Sub-problem 2: Compute the uncertainty ellipsoid

For sub-problem 1, perturb the angles and the strength and compute the 
uncertainty ellipsoid

- For each position there are several trajectories with different travel times
  and accuracy
  - E.g., shooting the ball high in the air has longer travel time and
    also likely a larger ellipsoid
  - Hitting straight has shorter travel time but it risks to go in the net
    and a certain ellipsoid

## Sub-problem 2
- Given the position of a ball and its uncertainty ellipsoid compute the
  probability that is in the court
  - This is just an integral (ok to solve it with Montercarlo)

## Sub-problem 3

- Given the position of a ball and its uncertainty ellipsoid compute the
  probability that the opponent can reach it (given the position, the travel time
  of the ball, the speed of the player)
  - Use Montecarlo

## Sub-problem 4

- Solve the problem with a grid
  - for each point we compute Montecarlo probability of the ball to be in and the
    probability (really 0 or 1) of the player to reach it 

## Problem 3: Where / how to serve?
Same thing for serving and responding 

## Problem 4: Where / how to respond to a serve
Same problem as above


## Problem 2: Where to move next?
Where should we move given where the opponent can throw the ball
- Game theory / reinforcement learning

Then we introduce the game theoretical part, since hitting a position might have
a larger probability of the opponent to reach it but also a higher probability
for the opponent to place it in a part where it’s not reachable

- Solve it for both tennis and pickleball since the only difference is the max ball speed


# Simulations and Results

# State of the Art
https://claude.ai/share/69dd11b7-08e0-47e4-9f78-4f26cef3d230
