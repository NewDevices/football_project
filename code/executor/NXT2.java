package org.lejos.pcexample;

import lejos.nxt.Motor;

/**
 * @author Timo Schrijvers
 * @author Hendrik Werner
 */

public class NXT2 {
    // Time needed to turn approximately 1 degree
    final static int turnTime = 22;
    // Time needed to give the motors the right speed
    final static int startTurnTime = 20;
    // Time needed to drive approximately 1 milimeter
    final static int driveTime = 24;
    // Time needed to give the motors the right speed
    final static int startDriveTime = 15;
    // Time needed to lower or upper the catch bar
    final static int catchTime = 1200;

    /**
     * The NXT robot will turn left for the amount of degrees that is given with
     * the parameter degree.
     */
    public static void turnLeft(int degree) {
        Motor.B.backward();
        Motor.C.forward();
        turn(degree);
    }

    /**
     * The NXT robot will turn right for the amount of degrees that is given
     * with the parameter degree.
     */
    public static void turnRight(int degree) {
        Motor.B.forward();
        Motor.C.backward();
        turn(degree);
    }

    /**
     * The NXT robot will continue for the amount of degrees that is given in
     * the parameter and stop after.
     */
    public static void turn(int degree) {
        try {
            Thread.sleep(turnTime * (degree + startTurnTime));
        } catch (InterruptedException e) {
            System.out.println("The sleep was interrupted.");
        } finally {
            Motor.B.stop();
            Motor.C.stop();
        }
    }

    /**
     * The robot will drive in a given direction for a particular distance.
     *
     * @param distance distance the robot will drive in milimeters
     * @param forward If true the robot will drive forwards, else it will drive
     * backwards
     */
    public static void drive(int distance, boolean forward) {
        if (forward) {
            Motor.B.forward();
            Motor.C.forward();
        } else {
            Motor.B.backward();
            Motor.C.backward();
        }
        try {
            Thread.sleep(driveTime * (distance + startDriveTime));
        } catch (InterruptedException e) {
            System.out.println("The sleep was interrupted.");
        } finally {
            Motor.B.stop();
            Motor.C.stop();
        }
    }

    /**
     * Turn the ballcatcher at the front of the robot up or down. If the catcher
     * is already down, or up it cannot go further in that direction.
     *
     * @param down If true, then the catcher will go down, else it will go up
     */
    public static void turn(boolean down) {
        if (down) {
            Motor.A.forward();
        } else {
            Motor.A.backward();
        }
        try {
            Thread.sleep(catchTime);
        } catch (InterruptedException e) {
            System.out.println("The sleep was interrupted.");
        } finally {
            Motor.A.stop();
        }
    }

    public static void main(String[] args) {
        Motor.A.setSpeed(50);
        Motor.B.setSpeed(100);
        Motor.C.setSpeed(100);
        if (args[0].equals("forward")) {
            drive(Integer.valueOf(args[1]), true);
        } else if (args[0].equals("backward")) {
            drive(Integer.valueOf(args[1]), false);
        } else if (args[0].equals("left")) {
            turnLeft(Integer.valueOf(args[1]));
        } else if (args[0].equals("right")) {
            turnRight(Integer.valueOf(args[1]));
        } else if (args[0].equals("up")) {
            turn(false);
        } else if (args[0].equals("down")) {
            turn(true);
        }
        System.out.println("done");
    }
}
