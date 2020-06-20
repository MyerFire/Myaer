"""
MIT License

Copyright (c) 2020 MyerFire

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import core.caches.friends
import ratelimit
import core.minecraft.request
import core.minecraft.hypixel.request
import core.minecraft.hypixel.static.static

async def get_status(uuid):
	try:
		status_json = (await core.minecraft.hypixel.request.get_status_by_uuid(uuid))
	except NameError:
		raise NameError("Invalid UUID")
	except ratelimit.RateLimitException:
		raise OverflowError # idk how to make custom exceptions so this is close enough

	status = {
		"online" : status_json.get("session", {}).get("online", False),
		"session" : {
			"game" : status_json.get("session", {}).get("gameType", ""),
			"instance" : status_json.get("session", {}).get("mode", "")
		}
	}
	return status
