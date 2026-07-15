Approximation 1
- 1D (like pong)
- The ball hits the baseline

Player model 1
- Model two pickleball players in terms of:
  - speed in movements
  - precision
    - The player wants to hit position x, but there is a std dev
  - how good their shots are
    - Compute prob of unforced error
    - This influence the strategy since knowing the opponent is bad
      suggests to just play without taking risks

Player model 2
  - how good is forehand (prob of unforced error)
  - how good is backhand (prob of unforced error)

Representation
- Position of each player on the base line $x$
- Each player needs to decide where to hit

Assumption 1
- They both know each other characteristics
  - Relax this assumption (-> learn model)

Model baseline rallies using RL
- What is the best strategies to win?
