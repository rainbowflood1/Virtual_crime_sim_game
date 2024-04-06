# load
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader
from ursina.shaders.screenspace_shaders.fxaa import *
from ursina.shaders.screenspace_shaders.ssao import *
from ursina.shaders import unlit_shader
from panda3d.core import LVecBase3f
from panda3d.core import NodePath
from panda3d.core import Fog
from panda3d.core import *
from direct.task import Task
from direct.filter.CommonFilters import CommonFilters
from direct.actor.Actor import Actor
from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
from panda3d.ai import *
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import ColorAttrib
from panda3d.core import Material
import numpy as np
import random
from ursina import *
from ursina.shaders import fxaa_shader

























Entity.default_shader = basic_lighting_shader
app =  Ursina()
gun_shot = Audio("files/audio/pistol_shot.mp3", autoplay=False)
gun_shot.volume = 0.5
falling = Audio("files/audio/wind-blowing.mp3", autoplay=False)
wanted = Text('', origin=(0, -10))
ammo = Text('', origin=(-8.5, 5))
chat = Text('', origin=(0, 10))
money_text = Text('<green>Money: 0', origin=(1, 5))
Sky = Entity(model="files/models/skysphere.egg", scale=8000, shader=unlit_shader, texture="files/image/sky/sunflowers_puresky_8k.hdr")
#sky = Sky(texture='sky_sunset')
camera.fov = 70

class game_data:
    step = 0
    game_full_screen = False
    screen_count = 0
    keyboard_toggle = False
    text = ""
    zoom = False
    shot = 0
    inches_per_360_degrees = 3.47222
    mouse_dpi = 800
    fov_degrees = camera.fov
    scaling_factor = 30000
    fov_radians = math.radians(fov_degrees)
    look_y = 0
    
ursina_sensitivity = ((game_data.inches_per_360_degrees / (game_data.mouse_dpi * math.tan(game_data.fov_radians / 2))) * game_data.scaling_factor)
sens = [ursina_sensitivity, ursina_sensitivity]
class Player_character(Entity):
    y_pos_is_looking_way_down = False
    y_pos_is_looking_down = False
    y_pos = 0
    grounded = False
    idle = False
    shake_multiplier = 1
    fall = True
    fell_time = 0
    reload = Audio("files/audio/pistol-reload.mp3", autoplay=False)
    xp = 0
    interacted = False
    money = 0
    crimes = []
    ready_fire = True
    ammo = 16
    max_ammo = 16
    player = FirstPersonController(position=(-200, 0, 0), collider='capsule')
    pistol = Entity(parent=camera, model="files/models/Pistol.fbx", position=(camera.X, camera.Y, camera.Z), scale=(0.001, 0.001, 0.001), rotation=(0, 180, 0), color=color.gray, collider="mesh", cooldown=False, shader=basic_lighting_shader)
    default_input = {}
    @property
    def hp(self):
        return None
    def __init__(self):
        self.player.mouse_sensitivity = sens
        self.player.speed = 10
player = Player_character()
camera_shake = Entity()










player.player.jump_height = 5
player.player.jump_up_duration = 1
player.player.cursor.color = rgb(0, 0, 0)
player.player.cursor.scale = 0.008-0.001
player.player.cursor.rotation_z = 0
money = Entity(model="files/models/money.fbx", color=color.green, position=(-200, 5, 0), scale=(0.001, 0.001, 0.001), rotation=(0, 180, 0), cooldown=False)
def player_update():
    if player.player.grounded == False:
        player.fall = True
        player.fell_time += 1
        falling.volume = (player.fell_time/60)*0.1
        camera.shake(duration=.1, magnitude=(player.fell_time/60)*2, speed=.01, direction=(1,1), delay=0, attr_name='rotation', interrupt='finish', unscaled=False)
    elif player.fall == True:
        player.fall = False
        falling.play()
    elif player.player.grounded == True:
        falling.volume = 0
        player.fall = False
        player.fell_time = 0
#camera_shake.update = player_update
def text_erase(var):
    var.text = ""
def shoot():
    if mouse.hovered_entity and player.ammo >= 1 and Player_character.pistol.cooldown == False:
        Player_character.pistol.cooldown = True
        Player_character.ready_fire = False
        print(f'shot and {player.ammo} left')
        gun_shot.play()
        invoke(setattr, Player_character.pistol, 'cooldown', False, delay=0.25)
        Player_character.ready_fire = True
        player.ammo -= 1
        print(mouse.world_point)
        ammo.text = f'{player.ammo}/{player.max_ammo}'
    elif player.ammo >= 1 and Player_character.pistol.cooldown == False:
        Player_character.pistol.cooldown = True
        Player_character.ready_fire = False
        print(f'shot and {player.ammo} left')
        gun_shot.play()
        invoke(setattr, Player_character.pistol, 'cooldown', False, delay=0.25)
        Player_character.ready_fire = True
        player.ammo -= 1
        ammo.text = f'{player.ammo}/{player.max_ammo}'
ocean_sine_x = np.linspace(0, 5, 201)
ocean_sine_y = np.sin(ocean_sine_x)
breath_sine_x = np.linspace(0, 5, 201)
breath_sine_y = np.sin(ocean_sine_x)
def update_ocean():
    if game_data.step == len(ocean_sine_y)-1:
        game_data.step = 0
    ocean.position = (0, ocean.Y + ocean_sine_y[game_data.step], 0)
    game_data.step += 1
class Car(Entity):
    def __init__(self, **kwargs):
        super().__init__(scale=(3, 1, 1), model="cube", collider="mesh", **kwargs)
car = Car(position=(-267.147, 5.09804, -38.0197))
rug = Entity(model="cube", position=(428.842, 5.09804, -440.25), scale=(2, 0.1, 5), collider="mesh", texture="files/image/texture/Fabric.jpg")
city = Entity(model="cube", position=(-358.303, 5.19804, -368.818), scale=(100, 0.1, 100), collider="mesh", color=color.gray)
tower = Entity(model="cube", position=(-391.209, 5.24804, -324.462), scale=(10, 100, 10), collider="mesh", color=color.cyan)
tower2 = Entity(model="cube", position=(-391.947, 5.24804, -344.097), scale=(10, 100, 10), collider="mesh", color=color.cyan)
tower3 = Entity(model="cube", position=(-371.947, 5.24804, -344.097), scale=(10, 100, 10), collider="mesh", color=color.cyan)
tower4 = Entity(model="cube", position=(-371.947, 5.24804, -324.462), scale=(10, 100, 10), collider="mesh", color=color.cyan)
road = Entity(model="cube", position=(-401.144, 5.24804, -368.818), scale=(5, 0.1, 100), collider="mesh", color=color.black)
dumpster = Entity(model="files/models/dumpster.egg", position=(-391.178, 6.24804, -337.74), scale=(1, 1, 1), rotation=(0, 90, 0), collider="mesh", color=color.green)
dumpster2 = Entity(model="files/models/dumpster.egg", position=(-371.54, 6.24804, -337.633), scale=(1, 1, 1), rotation=(0, 90, 0), collider="mesh", color=color.green)
dumpster3 = Entity(model="files/models/dumpster.egg", position=(-372.36, 6.24804, -330.976), scale=(1, 1, 1), rotation=(0, -90, 0), collider="mesh", color=color.green)
dumpster4 = Entity(model="files/models/dumpster.egg", position=(-391.946, 6.24804, -330.976), scale=(1, 1, 1), rotation=(0, -90, 0), collider="mesh", color=color.green)
terrain_entity = Entity(model=Terrain('./map_heightmap.png', skip=int(1000/100)), collider='mesh', scale=(1000, 50, 1000), position=(0, -10, 0), texture="map_texture_map")
def update():
    shader = Shader(language=Shader.GLSL, fragment='''
    #version 140


    vec3 sphere[16] = vec3[](
        vec3( 0.5381, 0.1856,-0.4319), vec3( 0.1379, 0.2486, 0.4430),
        vec3( 0.3371, 0.5679,-0.0057), vec3(-0.6999,-0.0451,-0.0019),
        vec3( 0.0689,-0.1598,-0.8547), vec3( 0.0560, 0.0069,-0.1843),
        vec3(-0.0146, 0.1402, 0.0762), vec3( 0.0100,-0.1924,-0.0344),
        vec3(-0.3577,-0.5301,-0.4358), vec3(-0.3169, 0.1063, 0.0158),
        vec3( 0.0103,-0.5869, 0.0046), vec3(-0.0897,-0.4940, 0.3287),
        vec3( 0.7119,-0.0154,-0.0918), vec3(-0.0533, 0.0596,-0.5411),
        vec3( 0.0352,-0.0631, 0.5460), vec3(-0.4776, 0.2847,-0.0271)
    );


    uniform sampler2D tex;
    uniform sampler2D dtex;
    uniform sampler2D random_texture;
    uniform mat4 p3d_ViewProjectionMatrix;

    in vec2 uv;
    out vec4 o_color;

    uniform float numsamples;
    uniform float radius;
    uniform float amount;
    uniform float strength;
    uniform float falloff;
    uniform float look_y;
    uniform float sens;


    vec3 get_normal(vec2 texcoords) {
        const vec2 offset1 = vec2(0.0, 0.001);
        const vec2 offset2 = vec2(0.001, 0.0);

        float depth = texture(dtex, texcoords).r;
        float depth1 = texture(dtex, texcoords + offset1).r;
        float depth2 = texture(dtex, texcoords + offset2).r;

        vec3 p1 = vec3(offset1, depth1 - depth);
        vec3 p2 = vec3(offset2, depth2 - depth);

        vec3 normal = cross(p1, p2);
        normal.z = -normal.z;

        return normalize(normal);
    }

    vec3 reconstructPosition(in vec2 uv, in float z)
    {
        float x = uv.x * 2.0f - 1.0f;
        float y = (1.0 - uv.y) * 2.0f - 1.0f;
        vec4 position_s = vec4(x, y, z, 1.0f);
        mat4x4 view_projection_matrix_inverse = inverse(p3d_ViewProjectionMatrix);
        vec4 position_v = view_projection_matrix_inverse * position_s;
        return position_v.xyz / position_v.w;
    }


    void main() {
        float depth = texture(dtex, uv).r;
        vec3 position = reconstructPosition(uv, depth);
        vec3 normal = get_normal(uv);

        vec2 noiseScale = vec2(800.0/4.0, 600.0/4.0); // screen = 800x600
        vec3 randomVec = texture(random_texture, uv * noiseScale).xyz;
        vec3 tangent   = normalize(randomVec - normal * dot(randomVec, normal));
        vec3 bitangent = cross(normal, tangent);
        mat3 TBN       = mat3(tangent, bitangent, normal);

        int iterations = 10;
        float size_per_iter = 0.001;
        float samples = 0.96;
        vec2 uv_reflection = vec2(uv.x, uv.y);

        for (int i = 0; i < iterations; i++) {
            if (texture(dtex, uv).r <= samples) {
                uv_reflection = vec2(uv.x+normal.r, (((-uv.y+normal.b)-size_per_iter*iterations)+normal.g-0.4)+look_y*sens*0.89);
                if (uv_reflection.y >= 1) {
                    uv_reflection = vec2(uv.x, uv.y);
                }
                if (normal.r >= 0.5) {
                    uv_reflection = vec2(uv.x-normal.r, (((uv.y+normal.b)-size_per_iter*iterations)+normal.g)-look_y*sens*0.1);
                }
            } else {
                size_per_iter = size_per_iter/2;
                //uv_reflection = vec2(uv.x, uv.y);
            }
        }

        o_color.rgb = o_color.rgb = (texture(tex, uv).rgb + texture(tex, uv_reflection).rgb/5).rgb;
        uv_reflection = vec2(uv.x, uv.y);
        //if (distance(texture(tex, uv).rgb, vec3(1, 1, 1)) > 0.2) {
        //    o_color.rgb = texture(tex, uv).rgb;
        //}
        
        //o_color.rgb = get_normal(uv + ray.xy).xzy;
        //o_color.rgb = texture(tex, uv_reflection).rgb;
        o_color.a = 1.0;
    }
    ''',

    default_input = {
        'numsamples' : 64*2,
        'radius' : 0.01, # 0.05 is broken and cool
        'amount' : 3.0,
        'strength' : 0.001,
        'falloff' : 0.000002,
        'random_texture' : Func(load_texture, 'noise'),
        'look_y': player.player.camera_pivot.rotation_x/90,
        'sens': game_data.inches_per_360_degrees
    }
    )
    camera.shader = shader
    print((player.player.camera_pivot.rotation_x/90))
    player.y_pos = player.player.camera_pivot.rotation_x
    player.y_pos_is_looking_down = player.player.camera_pivot.rotation_x >= 0.7
    player.y_pos_is_looking_way_down = player.player.camera_pivot.rotation_x >= 90.0
    print(player.y_pos_is_looking_down)
    #camera.rotation += ((breath_sine_y[game_data.step]*0.001)*player.shake_multiplier, (breath_sine_y[game_data.step]*0.005)*player.shake_multiplier, 0)
    if held_keys['left mouse'] and Player_character.ready_fire == True:
        shoot()
        #camera.shake(duration=.1, magnitude=2, speed=.01, direction=(1,1), delay=0, attr_name='rotation', interrupt='finish', unscaled=False)
    elif held_keys["e"]:
        interact_ray = raycast(Player_character.player.camera_pivot.world_position, Player_character.player.camera_pivot.world_rotation, ignore=(player.player,))
        if interact_ray.hit:
            print(type(interact_ray.entity))
    elif held_keys["r"]:
        Player_character.pistol.cooldown = True
        Player_character.ready_fire == False
        Player_character.reload.play()
        invoke(setattr, Player_character.pistol, 'cooldown', False, delay=1)
        player.ammo = player.max_ammo
        ammo.text = f'{player.ammo}/{player.max_ammo}'
        Player_character.ready_fire == True
    elif player.ammo == 0:
        ammo.text = f'<red>{player.ammo}<default>/{player.max_ammo}'
    elif held_keys["shift"]:
        Player_character.player.speed = 200
        player.shake_multiplier = 5
        #player.player.y += 15
    elif not held_keys["shift"]:
        Player_character.player.speed = 10
        player.shake_multiplier = 1
        
#ground = Entity(model="cube", position=(0, -100, 0), scale=(50, 10, 50), collider="mesh", texture="files/image/texture/grass.png", shader=basic_lighting_shader)
ocean = Entity(model="plane", position=(0, 0, 0), color=color.cyan, scale=(5000, 1, 5000))






ocean.update = update_ocean
pivot = Entity()
Player_character.player.y = 15
app.run()
