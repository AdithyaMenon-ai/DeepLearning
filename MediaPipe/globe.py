import cv2
import mediapipe as mp
import trimesh
import pyglet
from pyglet.gl import *

# ---------------- Hand Tracking ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
cap = cv2.VideoCapture(0)

rot_x, rot_y = 0, 0
prev_x, prev_y = None, None

# ---------------- Load GLB ----------------
scene = trimesh.load("globe.glb")
mesh = scene.dump().sum()

vertices = mesh.vertices.flatten()
faces = mesh.faces.flatten()

# ---------------- Pyglet Window ----------------
window = pyglet.window.Window(800, 600, "GLB Globe – Hand Controlled")

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0, 0, -3)
    glRotatef(rot_x, 1, 0, 0)
    glRotatef(rot_y, 0, 1, 0)

    glBegin(GL_TRIANGLES)
    for f in faces:
        v = vertices[f*3:f*3+3]
        glVertex3f(*v)
    glEnd()

def update(dt):
    global rot_x, rot_y, prev_x, prev_y

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        lm = result.multi_hand_landmarks[0].landmark
        h, w, _ = frame.shape
        x = int(lm[8].x * w)
        y = int(lm[8].y * h)

        if prev_x is not None:
            rot_y += (x - prev_x) * 0.3
            rot_x += (y - prev_y) * 0.3

        prev_x, prev_y = x, y

    cv2.imshow("Hand Tracker", frame)
    cv2.waitKey(1)

glEnable(GL_DEPTH_TEST)
pyglet.clock.schedule(update)
pyglet.app.run()
