#!/usr/bin/env python
# coding: utf-8

# In[3]:


import time
import math
import keyboard  # For detecting the ESC key

def calculate_rotational_params(t1, t2):
    """
    Calculate rotational deceleration and initial rotational velocity.
    """
    try:
        rda = 4 * math.pi * (2 * t1 - t2) / (t2 * t1 * (t2 - t1))  # Rotational deceleration (rads/s^2)
        rv0a = (4 * math.pi - rda * t1**2) / (2 * t1)  # Initial rotational velocity (rads/s)
        return rda, rv0a
    except ZeroDivisionError:
        print("Error: Division by zero occurred. Please ensure timing intervals are valid.")
        return None, None

def calculate_stop_angle(rda, rv0a):
    """
    Calculate stop angle based on deceleration and initial velocity.
    """
    try:
        tn = -rv0a / rda  # Time to stop
        sa = rv0a * tn + 0.5 * rda * tn**2  # Stop angle
        return sa % (2 * math.pi)  # Normalize to [0, 2π)
    except ZeroDivisionError:
        print("Error: Division by zero in stop angle calculation.")
        return None

def map_angle_to_bet(sa_deg):
    """
    Map the stop angle in degrees to a roulette number.
    """
    bet_values = [
        0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
        6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
        24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
        29, 7, 28, 12, 35, 3, 26
    ]
    segment_size = 360 / 37  # Degrees per segment
    idx = int(sa_deg / segment_size)
    return bet_values[idx]

def main():
    print("Welcome to the Rotational Simulation!")
    print("Press ESC to exit the simulation at any time.\n")
    
    while True:
        try:
            # Check if ESC key is pressed
            if keyboard.is_pressed('esc'):
                print("\nExiting the simulation. Goodbye!")
                break
            
            print("\nPress Enter each time the ball passes 0...")
            
            # Timing inputs
            input("Press Enter for the first pass at 0:")
            start_time = time.time()
            
            input("Press Enter for the second pass at 0:")
            t1 = time.time() - start_time
            
            input("Press Enter for the third pass at 0:")
            t2 = time.time() - start_time
            
            # Calculate rotational parameters
            rda, rv0a = calculate_rotational_params(t1, t2)
            
            if rda is None or rv0a is None:
                print("Failed to calculate rotational parameters. Try again.")
                continue
            
            # Ensure the ball is decelerating
            if rda < 0:
                # Calculate stop angle
                sa = calculate_stop_angle(rda, rv0a)
                if sa is None:
                    continue
                sa_deg = math.degrees(sa)  # Convert to degrees
                
                # Map angle to roulette bet
                bet = map_angle_to_bet(sa_deg)
                print(f"\nRotational deceleration: {rda:.4f} rad/s²")
                print(f"Initial rotational velocity: {rv0a:.4f} rad/s")
                print(f"Predicted stop angle: {sa_deg:.2f}°")
                print(f"Roulette number: {bet}")
            else:
                print("Not Possible: Ball does not decelerate.")
        
        except KeyboardInterrupt:
            print("\nExiting the simulation. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()


# In[2]:


# need to have // pip install keyboard

