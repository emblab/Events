<%!
	bodycls = 'event'
	title   = u'Event in BaToReL'
%>
<%inherit file="_templates/batorel.mako" />

<div class="event-owner">
	<div class="avatar-container"><img src="/events/img/${event['Host']}" alt="(${event['Nickname']})" /></div>
	<div class="nickname-container">${event['Nickname']}</div>
</div>
<h2>Event „${event['Title']}“</h2>

<dl class="event-basics">
	<dt>Start:</dt><dd>${event['.StartDate']}</dd>
	<dt>Ende:</dt><dd>${event['.EndDate']}</dd>
	<dt>Ort:</dt><dd><a href="http://maps.google.com/maps?q=${event['Latitude']},${event['Longitude']}+(Dan)">${event['LocationName']}</a></dd>
</dl>
<div class="event-description">
	<p>
	${event['Activity']}
	% if event['PartySize'] > 0:
	(maximal ${event['PartySize']} Teilnehmer)
	% endif
	</p>
</div>

<p style="margin-top: 2em">
Möchtest du teilnehmen? Dann lade dir BaToReL herunter!
</p>
<div class="center-button">${self.button("Download", "download.html", "download")}</div>
