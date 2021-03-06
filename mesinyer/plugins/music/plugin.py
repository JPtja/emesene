import gobject

import extension
import songretriever
import Preferences

from plugin_base import PluginBase

class Plugin(PluginBase):
    def __init__(self):
        PluginBase.__init__(self)
        self.session = None
        self.player = "mpd"
        self.format = "%ARTIST% - %ALBUM% - %TITLE%"
        self.running = False
        self.last_title = None

    def start(self, session):
        '''start the plugin'''
        self.session = session
        self.running = True
        gobject.timeout_add(500, self.check_song)
        return True

    def stop(self):
        '''start the plugin'''
        self.session = None
        self.running = False
        return True

    def config(self, session):
        '''config the plugin'''
        Preferences.Preferences(self._on_config, self.player,
                self.format).show()

    def _on_config(self, status, player, format):
        '''callback for the config dialog'''
        if status:
            self.player = player
            self.format = format

    def check_song(self):
        '''get the current song and set it if different than the last one'''

        if self.session:
            song = songretriever.get_current_song(self.player)

            if song:
                current_title = song.format(self.format)
                if current_title != self.last_title:
                    self.session.set_media(current_title)
                    self.last_title = current_title
            elif self.last_title is not None:
                self.last_title = None
                self.session.set_media("not playing")

        return self.running

