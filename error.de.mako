<%!
	lang    = 'de'
	bodycls = 'error'
	title   = u'BaToReL Fehler'
%>
<%inherit file="_templates/batorel.mako" />

<h2>Fehler</h2>

<p>
Sorry, wir können dir diesen Event nicht anzeigen, denn:
</p>

<p style="font-weight: bold">
<strong>${error}</strong>
</p>
