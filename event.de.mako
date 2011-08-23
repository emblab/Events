<%!
	lang    = 'de'
	bodycls = 'event'
	title   = u'Event in BaToReL'
%>
<%inherit file="_templates/batorel.mako" />

<div class="event-owner">
	<div class="avatar-container"><img src="/events/img/${event['Host']}" alt="(${event['Nickname']})" /></div>
	<div class="nickname-container">${event['Nickname']}</div>
</div>
<h2>Event “${event['Title']}“</h2>

<dl class="event-basics">
	<dt>Start:</dt><dd>${event['.StartDate']}</dd>
	<dt>End:</dt><dd>${event['.EndDate']}</dd>
	<dt>Location:</dt><dd><a href="http://maps.google.com/maps?q=${event['Latitude']},${event['Longitude']}+(${event['Title']})">${event['LocationName']}</a></dd>
	<dt>Activity:</dt><dd>${event['Activity']}</dd>
	% if event['PartySize'] > 0:
        <dt>Participants:</dt><dd>max ${event['PartySize']}</dd>
        % endif


</dl>
<div class="event-description">
	<p>
	% if event['Description'] and len(event['Description']) > 0:
	Description:<br> ${event['Description']}
	% endif
	</p>
</div>

<p style="margin-top: 2em">
Möchtest du teilnehmen? Dann lade dir BaToReL herunter!
</p>
<div class="center-button">${self.button("Download", "download.html", "download")}</div>
