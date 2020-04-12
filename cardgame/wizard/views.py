from django.shortcuts import redirect, render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def index(request):
    return render(request, 'wizard/index.html')


def join(request):
    return redirect('game', name=request.GET['game'])


def game(request, name):
    return render(request, 'wizard/game.html', {"name": name})


def say(request, name, text):
    channel_layer = get_channel_layer()
    group_name = "wizard_" + name
    print(text, "->", group_name)
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'game_message',
            'message': text
        }
    )

    return render(request, 'wizard/blank.html', {"name": name})
