import pygame
from creature import *


class Damager(Creature):
    def __init__(self):
        super().__init__()
        self.TTL = 100
        self.disappear = False
        self.parent_id = 0
        self.pierce = False
        self.max_pierce = 12
        self.pierce_count = 0
        self.attack_power = 0
        self.attack_properties = None

        self.leave_particles = False
        self.leave_particles_counter = 0
        self.leave_particles_every_x_tick = 1  # damager leaves trail
        self.leave_hole = False
        self.leave_hole_at_obstacle = None
        self.need_to_leave_particle = False
        self.particle_radius = 0
        self.particle_fly_speed = 0
        self.particle_destination = None
        self.particle_TTL = 0
        self.particle_gravity_affected = False
        self.particle_fade_out_speed = 1
        self.particles_quantity = 1
        self.particles_quantity_counter = 0
        self.particles_color = None



    def process(self, time_passed):
        if self.TTL == 0:
            self.disappear = True
            return
        elif self.TTL > 0:
            self.TTL -= 1
        if self.wait_counter > 0:
            self.wait_counter -= 1
            return
        self.move(time_passed)
        if self.leave_particles:
            if self.particles_quantity_counter < self.particles_quantity:
                self.leave_particles_counter += 1
                if self.leave_particles_counter == self.leave_particles_every_x_tick:
                    self.particles_quantity_counter += 1
                    self.need_to_leave_particle = True
                    self.leave_particles_counter = 0
        if self.max_fly_speed > self.fly_speed_reduce:
            self.max_fly_speed -= self.fly_speed_reduce
        if self.destination_reached:
            self.get_suicide()

    def get_suicide(self):
        self.disappear = True

