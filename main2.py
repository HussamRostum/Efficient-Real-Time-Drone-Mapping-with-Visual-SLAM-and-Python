import env,sensors
import pygame # type: ignore
import math

environment = env.buildEnvironment((600,1200))
environment.originalMap = environment.map.copy()
laser = sensors.LaserSensor(200,environment.originalMap,uncetainty=(0.5,0.01))
environment.map.fill((255,255,255))
environment.infomap = environment.map.copy()

running = True
while running :
    sensorON = False
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_focused():
            sensorON = True
        elif not pygame.mouse.get_focused():
            sensorON = False
    if sensorON:
        position = pygame.mouse.get_pos()
        laser.position = position
        sensor_data = laser.sense_obstacles()
        environment.datastorage(sensor_data)
        environment.show_sensorData()
    environment.map.blit(environment.infomap,(0,0))
    pygame.display.update()
