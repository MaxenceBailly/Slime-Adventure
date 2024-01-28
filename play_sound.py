import winsound, random
def play_sound(sound):
    sound_list = {'slime_jump':['Slime Adventure\sounds\slime_jump2.wav'], 'slime_on_surface':['Slime Adventure\sounds\slime_on_surface2.wav']}
    if sound in sound_list.keys():
        winsound.PlaySound(random.choice(sound_list[sound]), winsound.SND_FILENAME | winsound.SND_ASYNC)