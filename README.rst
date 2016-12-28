Recordium
=========

A simple app to help your *out-of-your-desktop-or-laptop* self to remind
stuff to your future *in-your-desktop-or-laptop* self.

The idea is that you execute Recordium in your desktop computer or in your
laptop, and it will remain there as a small icon.

.. image:: https://raw.githubusercontent.com/facundobatista/recordium/master/media/icon-192.png

Later, anytime, you are on the road or away, and remind something you should
do in the future. At that moment you send a Telegram text or audio to your
Recordium Bot. And when you come back to your computer (where you can take
proper actions for the reminder), the Recordium icon will be light up, and
you see that message there.


Step by step instructions
-------------------------

- Set up Recordium (provisional instructions, in the future this should be
  packaged)::

    git clone git@github.com:facundobatista/recordium.git
    cd recordium
    bin/recordium

- Create a telegram bot

  - Open your telegram client

  - Talk to BotFather

  - Use the /newbot command to create a new bot. The BotFather will ask you
    for a name and username, then generate an authorization token for your
    new bot.

  - For better detailed instructions, see
    `here <https://core.telegram.org/bots>`_.

- Configure Recordium properly

  - Click on the Recordium icon, select "Configure"

  - Put the bot auth token there


F.A.Q.
------

- **Wait, couldn't you almost solve this using other propietary and/or more
  complex tools?** Probably yes, but I didn't want more complex stuff (and
  no way using Google for this). Also, and it's the most important reason: I
  wanted a toy project for using PyQt 5 under Python 3.

- **Is there a way to debug what it does?** When running ``bin/recordium``
  see that it tells you where logs are kept. Also, you can do
  ``bin/recordium -v`` and see it all in the terminal.
