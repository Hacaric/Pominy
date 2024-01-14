from easygame import *
import socket
import errno
import sys
import math
from easygame_m import *
import time
HEADER_LENGTH = 10
timer = math.floor(time.time())
IP = input("input ip of the server, whitch you connecting: ")
PORT = 1234
my_username = input("Username: ")
width = 800
height = 600

fps = 60

open_window("Game whitch doesn't works (because Kung-Fu Panda)", width, height, fps = fps)

# Začni vykreslovať snímky v cykle (v predvolenej rýchlosti 60fps)
game_run = True

ground = 10

player_stay = load_image("assets/player/stay.png")
player_go = [load_image("assets/player/go_1.png"), load_image("assets/player/go_2.png")]

player_stay_2 = load_image("assets/player/stay2.png")
player_go_2 = [load_image("assets/player/go_12.png"), load_image("assets/player/go_22.png")]

player_stay_3 = load_image("assets/player/stay3.png")
player_go_3 = [load_image("assets/player/go_32.png"), load_image("assets/player/go_33.png")]

player_stay_4 = load_image("assets/player/stay4.png")
player_go_4 = [load_image("assets/player/go_41.png"), load_image("assets/player/go_42.png")]
player_img = player_stay_4
player_scale = 3

player_width = len(image_data(player_img)[0])
player_height = len(image_data(player_img))

player_vel_x = 0
player_vel_y = 0

player_pos = [0,0]

spd = 10

bg_img = load_image("assets/bg.png")
bg_height = len(image_data(bg_img))
bg_width = len(image_data(bg_img)[0])

bg_scale_x = 15
bg_scale_y = 15

player_dir = "S"

wall_x = [0 - bg_width * bg_scale_x, bg_width * bg_scale_x]
wall_y = [0 - bg_height * bg_scale_y, 850]

bg_pos = (wall_x[0], wall_y[0])
print(bg_pos)

set_camera((350,250), (0,0))

health_bar_img = load_image("assets/health_bar.png")

buttons = {
    "W": False,
    "S": False,
    "D": False,
    "A": False,
}

hit_fields = ["None", "None", "None", "None"]
maxhealth = 30
health = maxhealth

died_time = 0

hit_width = 70
hit_height = 70

delay_hit = 0

go = 0

def hit():
    print(player_dir)
    if delay_hit > 0:
        pass
    else:
        if player_dir == "W":
            hit_fields[0] = player_pos[0]
            hit_fields[1] = player_pos[1]+ player_height*player_scale
        elif player_dir == "S":
            hit_fields[0] = player_pos[0]
            hit_fields[1] = player_pos[1]- player_height*player_scale
        elif player_dir == "D":
            hit_fields[0] = player_pos[0]+ player_width*player_scale
            hit_fields[1] = player_pos[1]
        elif player_dir == "A":
            print(str(player_pos[0]) + ", " + str(player_width))
            hit_fields[0] = player_pos[0]- player_width*player_scale
            hit_fields[1] = player_pos[1]
        hit_fields[2] = hit_width
        hit_fields[3] = hit_height
hraci = []
# Začni vykreslovať snímky v cykle (v predvolenej rýchlosti 60fps)
should_quit = False

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
senddata = ""
receiveddata = []
 
# Začni vykreslovať snímky v cykle (v predvolenej rýchlosti 60fps)
while True:
 
    # Otvor okno s nadpisom "Panda simulator"
    # vo veľkosti 800px na šírku a 600px na výš
        # Wait for user to input a message
    message = senddata
        # Načítaj udalosti pre aktuálnu snímku


        


    # vo veľkosti 800px na šírku a 600px na výšku
    
    
    for event in poll_events(): 
        if type(event) is CloseEvent:
            game_run = False
            close_window()
            sys.exit()
            break
        if type(event) is KeyDownEvent:
            buttons[event.key] = True
            player_dir = event.key
        if type(event) is KeyUpEvent:
            buttons[event.key] = False
        if type(event) is MouseDownEvent:
            if event.button == "LEFT":
                hit()
                play_audio(load_audio("assets/punch.mp3"), 0)

    player_vel_x = 0
    player_vel_y = 0

    for but in buttons:
        if but == "W":
            if buttons[but] == True:
                player_vel_y = spd
                if go < 29:
                    player_img = player_go_3[0]
                elif go < 59:
                    player_img = player_go_3[1]
                else:
                    player_img = player_stay_3
                go += 1
                go = go % 90
        if but == "S":
            if buttons[but] == True:
                player_vel_y = 0 - spd
                if go < 29:
                    player_img = player_go_4[0]
                elif go < 59:
                    player_img = player_go_4[1]
                else:
                    player_img = player_stay_4
                go += 1
                go = go % 90
        if but == "D":
            if buttons[but] == True:
                player_vel_x = spd
                if go < 29:
                    player_img = player_go_2[0]
                else:
                    player_img = player_go_2[1]
                go += 1
                go = go % 50
        if but == "A":
            if buttons[but] == True:
                player_vel_x = 0 - spd
                if go < 29:
                    player_img = player_go[0]
                else:
                    player_img = player_go[1]
                go += 1
                go = go % 50



    
    bg_color(0,0,0)
    draw_image(bg_img, bg_pos, pixelated = True, scale = bg_scale_x * 2)
    if hit_fields[0] != "None":
        print(hit_fields)
        draw_rect(hit_fields[0], hit_fields[1], hit_fields[2], hit_fields[3], colorm=(1,1,1,1))
    if health > 0:
        last_pos = player_pos
        player_pos = [max(min(player_pos[0] + player_vel_x, wall_x[1] - player_width * player_scale), wall_x[0]), max(min(player_pos[1] + player_vel_y, wall_y[1] - player_width), wall_y[0])]
        move_camera((player_pos[0] - last_pos[0], player_pos[1] - last_pos[1]))
        draw_image(player_img, player_pos, scale =player_scale, pixelated = True)
    
    # Health bar
    draw_image(health_bar_img, (width - 250, height - 45), pixelated=True, ui = True, scale = 4)
    draw_rect(width - 195, height - 35,health * 7.5, 25, (1,0,0,1),ui = True)

    draw_text(f"{player_pos}", "Pixelify Sans", 12, position=(15, height - 50), color=(1,1,1,1), ui = True)


    
    if health <= 0:
        draw_text("YOU DIED", "Pixelify Sans", 50, position=(width / 2 - 150, height / 2), color=(1,0,0,1), ui = True)
        
        died_time += 1
        if died_time == fps * 3:
            close_window()
            sys.exit()
            game_run = False
    if len(hit_fields):
        senddata = str(player_pos[0]) + "," + str(player_pos[1]) + "," + str(hit_fields[0]) + "," + str(hit_fields[1])
    else:
        senddata = str(player_pos[0]) + "," + str(player_pos[1]) + "," + str(None) + "," + str(None)
    redvicedata = receiveddata
    for i in range(math.floor(len(redvicedata)/4)):
        draw_image(player_img, (int(redvicedata[i*4]),int(receiveddata[i*4+1])), scale =player_scale, pixelated = True)
        # * Next frame;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        if redvicedata[i*4 + 3] != "None":
            print(redvicedata[i*4+2])
            if (player_pos[0] > int(redvicedata[i*4+2]) and player_pos[0] < (int(redvicedata[i*4+2])+70)) and (player_pos[1] > (int(redvicedata[i*4+3])) and player_pos[1] < (int(redvicedata[i*4+3])+70)):
                health -= 0.1
    if (timer - math.floor(time.time())) % 3 == 0 and health < maxhealth:
        health += 0.0
    
    
    # * Next frame
    
    next_frame()

    # If message is not empty - send it
    if message != "":
        senddata = ""
        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                close_window()
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Print message
            receiveddata = message.split(",")
            print(f'{username} > {message}')

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            close_window()
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        close_window()
        sys.exit()