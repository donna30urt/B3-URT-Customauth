# ################################################################### #
#                                                                     #
#  BigBrotherBot(B3) (www.bigbrotherbot.net)                          #
#  Copyright (C) 2005 Michael "ThorN" Thornton                        #
#                                                                     #
#  This program is free software; you can redistribute it and/or      #
#  modify it under the terms of the GNU General Public License        #
#  as published by the Free Software Foundation; either version 2     #
#  of the License, or (at your option) any later version.             #
#                                                                     #
#  This program is distributed in the hope that it will be useful,    #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of     #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the       #
#  GNU General Public License for more details.                       #
#                                                                     #
#  You should have received a copy of the GNU General Public License  #
#  along with this program; if not, write to the Free Software        #
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA      #
#  02110-1301, USA.                                                   #
#                                                                     #
# ################################################################### #
__author__ = 'donna30' 
__version__ = '1.0'

import b3
import re
import b3.events
import b3.plugin

class CustomauthPlugin(b3.plugin.Plugin):
    requiresConfigFile = False

    #Getting Plugin admin (cannot register commands without it)
    def onStartup(self):
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return

        # Registering events
        self.registerEvent(self.console.getEventID('EVT_CLIENT_JOIN'), self.onJoin)
        # Registering commands
        self._adminPlugin.registerCommand(self, 'setauth', 2, self.cmd_customauth, 'customauth')
        self._adminPlugin.registerCommand(self, 'removeauth', 40, self.cmd_remauth, 'rmauth')

    def onJoin(self, event):
        client = event.client
        self.update_auth(client)

    def update_auth(self, client):
        if client.bot:
            self.debug('Bot')
        else:
            cursor = self.console.storage.query('SELECT * FROM cauth WHERE iduser = %s' % client.id)
            auth = str(cursor.getValue('auth'))
            cursor.close()
            if auth == 'None':
                return
            self.console.write('changeauth %s %s' % (client.cid, auth))

    def cmd_customauth(self, data, client, cmd=None):
        if not data:
            client.message('!setauth <auth>')
            return
        cursor = self.console.storage.query('SELECT * FROM cauth WHERE iduser = %s' % client.id)
        if cursor.rowcount == 0:
            handler = self._adminPlugin.parseUserCmd(data)
            value = str(handler[0])
            self.console.write('changeauth %s %s' % (client.cid, value))
            client.message('Auth set to: %s' % value)
            # \' converting into a string?
            cursor = self.console.storage.query('INSERT INTO cauth (iduser, auth) VALUES (%i, \'%s\')' % (client.id, value))
            cursor.close()
        else:
            client.message('Auth already existing')

    def cmd_remauth(self, data, client, cmd=None):
        if not data:
            client.message('!rmauth <client>')
            return
        handler = self._adminPlugin.parseUserCmd(data)
        sclient = self._adminPlugin.findClientPrompt(handler[0], client)
        if not sclient:
            client.message('client not found')
            return
        self.console.storage.query('DELETE cauth FROM cauth WHERE iduser = %s' % sclient.id)
        client.message('Removed the auth from %s' % sclient.name)
        sclient.message('Your auth has been removed')