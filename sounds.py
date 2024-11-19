# pygame.mixer.music.load
# 	Load a music file for playback
# pygame.mixer.music.unload
# 	Unload the currently loaded music to free up resources
# pygame.mixer.music.play
# 	Start the playback of the music stream
# pygame.mixer.music.rewind
# 	restart music
# pygame.mixer.music.stop
# 	stop the music playback
# pygame.mixer.music.pause
# 	temporarily stop music playback
# pygame.mixer.music.unpause
# 	resume paused music
# pygame.mixer.music.fadeout
# 	stop music playback after fading out
# pygame.mixer.music.set_volume
# 	set the music volume
# pygame.mixer.music.get_volume
# 	get the music volume
# pygame.mixer.music.get_busy
# 	check if the music stream is playing
# pygame.mixer.music.set_pos
# 	set position to play from
# pygame.mixer.music.get_pos
# 	get the music play time
# pygame.mixer.music.queue
# 	queue a sound file to follow the current
# pygame.mixer.music.set_endevent
# 	have the music send an event when playback stops
# pygame.mixer.music.get_endevent
# 	get the event a channel sends when playback stops

import pygame.mixer
from constants import MUSIC_VOLUME, SOUND_VOLUME

pygame.mixer.init()
# pygame.mixer.music.load('music/ambient_1.mp3')
pygame.mixer.music.set_volume(MUSIC_VOLUME)

sound_glass_blast_1 = pygame.mixer.Sound('SFX/blast_glass.mp3')
sound_glass_blast_1.set_volume(SOUND_VOLUME)
sound_step_1 = pygame.mixer.Sound('SFX/steps/tihiy-gluhoy-shag.wav')
sound_step_1.set_volume(SOUND_VOLUME)
sound_step_2 = pygame.mixer.Sound('SFX/steps/tihiy-gluhoy-shag_2.wav')
sound_step_2.set_volume(SOUND_VOLUME)
sound_swing_2 = pygame.mixer.Sound('SFX/swing.mp3')
sound_swing_2.set_volume(SOUND_VOLUME)
sound_reload = pygame.mixer.Sound('SFX/reload.mp3')
sound_reload.set_volume(SOUND_VOLUME)
sound_shotgun_shot = pygame.mixer.Sound('SFX/shots/shotgun_shot.mp3')
sound_shotgun_shot.set_volume(SOUND_VOLUME)
sound_pistol_shot = pygame.mixer.Sound('SFX/shots/pistol_shot_1.mp3')
sound_pistol_shot.set_volume(SOUND_VOLUME)
sound_jane_pain = pygame.mixer.Sound('SFX/shouts/jane_pain.mp3')
sound_jane_pain.set_volume(SOUND_VOLUME)
sound_jake_pain = pygame.mixer.Sound('SFX/shouts/jake_pain.mp3')
sound_jake_pain.set_volume(SOUND_VOLUME)
sound_demon_pain = pygame.mixer.Sound('SFX/shouts/demon_pain.mp3')
sound_demon_pain.set_volume(SOUND_VOLUME)
sound_click_4 = pygame.mixer.Sound('SFX/click_4.mp3')
sound_click_4.set_volume(SOUND_VOLUME)
sound_door_1 = pygame.mixer.Sound('SFX/door_1.mp3')
sound_door_1.set_volume(SOUND_VOLUME)
sound_meat_blow_1 = pygame.mixer.Sound('SFX/knife_blow.mp3')
sound_meat_blow_1.set_volume(SOUND_VOLUME)
sound_man_taunt_1 = pygame.mixer.Sound('SFX/shouts/man_taunt.mp3')
sound_man_taunt_1.set_volume(SOUND_VOLUME)
sound_bucket_hit_1 = pygame.mixer.Sound('SFX/bucket_hit.mp3')
sound_bucket_hit_1.set_volume(SOUND_VOLUME)
sound_bullet_wall_hit_1 = pygame.mixer.Sound('SFX/bullet_wall_hit.mp3')
sound_bullet_wall_hit_1.set_volume(SOUND_VOLUME)
sound_bounce_1 = pygame.mixer.Sound('SFX/bounce_1.mp3')
sound_bounce_1.set_volume(SOUND_VOLUME*2)
sound_groan_1 = pygame.mixer.Sound('SFX/shouts/man_groan_pain.mp3')
sound_groan_1.set_volume(SOUND_VOLUME*2)

sounds_all = {
    'sound_groan_1': sound_groan_1,
    'sound_bounce_1': sound_bounce_1,
    'sound_bullet_wall_hit_1': sound_bullet_wall_hit_1,
    'sound_bucket_hit_1': sound_bucket_hit_1,
    'sound_glass_blast_1': sound_glass_blast_1,
    'sound_man_taunt_1': sound_man_taunt_1,
    'sound_step_1': sound_step_1,
    'sound_step_2': sound_step_2,
    'sound_swing_2': sound_swing_2,
    'sound_reload': sound_reload,
    'sound_shotgun_shot': sound_shotgun_shot,
    'sound_pistol_shot': sound_pistol_shot,
    'sound_jane_pain': sound_jane_pain,
    'sound_jake_pain': sound_jake_pain,
    'sound_demon_pain': sound_demon_pain,
    'sound_click_4': sound_click_4,
    'sound_meat_blow_1': sound_meat_blow_1,
    'sound_door_1': sound_door_1,
    # 'sound_step_1': sound_step_1,
    # 'sound_step_2': sound_step_2,
    # 'sound_swing_2': sound_swing_2,
    # 'sound_reload': sound_reload,
    # 'sound_shotgun_shot': sound_shotgun_shot,
    # 'sound_pistol_shot': sound_pistol_shot,
    # 'sound_jane_pain': sound_jane_pain,
    # 'sound_jake_pain': sound_jake_pain,
    # 'sound_demon_pain': sound_demon_pain,
    # 'sound_click_4': sound_click_4,
    # 'sound_meat_blow_1': sound_meat_blow_1,
    # 'sound_door_1': sound_door_1
}
sound_all_steps = (sounds_all['sound_step_1'], sounds_all['sound_step_2'])
# ambient_1.set_volume(0.05)
# pygame.mixer.Sound.play(ambient_1)