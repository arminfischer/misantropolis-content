$feedItems = @()

# Get posts and generate JSON feed items
$posts = Invoke-RestMethod -Uri https://misantropolisstrg.blob.core.windows.net/data/posts.json
$posts | ForEach-Object { $feedItems += @{ "id" = $_.permalink; "date_published" = $_.date_gmt ; "title" = $_.title; "content_text" = $_.content; "url" = "https://www.misantropolis.de" + $_.permalink } }

Write-Host "$($posts.Count) posts downloaded"

# Assemble JSON feed and render to temporary file
$feed = @{ "version"            = "https://jsonfeed.org/version/1.1"; `
                "title"         = "misantropolis.de"; `
                "home_page_url" = "https://www.misantropolis.de/"; `
                "feed_url"      = "https://www.misantropolis.de/feed.json"; `
                "description"   = "Feed von Misanthrop auf misantropolis.de"; `
                "items"         = $feedItems 
}
$feed | ConvertTo-Json | Set-Content feed.json

Write-Host "JSON feed assembled"

# Assemble Atom feed and render to temporary file
$atom = @"
<?xml version="1.0" encoding="UTF-8" ?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>$($feed.title)</title>
  <subtitle>$($feed.description)</subtitle>
  <link href="$($feed.home_page_url)" />
"@
$feed.items | ForEach-Object { $atom += "<entry><id>$($_.id)</id><title>$([System.Web.HTTPUtility]::HtmlEncode($_.title))</title><link href=""$($_.url)"" /><content type=""xhtml""><![CDATA[$($_.content_text)]]></content><updated>$([Xml.XmlConvert]::ToString($_.date_published,[Xml.XmlDateTimeSerializationMode]::Utc))</updated></entry>" }
$atom += @"
</feed>
"@
$atom | Set-Content feed.xml

Write-Host "Atom feed assembled"

# Upload feeds to Azure Blob
az storage blob upload -c 'data' --account-name misantropolisstrg -f feed.xml -n feed.xml
az storage blob upload -c 'data' --account-name misantropolisstrg -f feed.json -n feed.json

Write-Host "Feeds uploaded"

# Clean up
Remove-Item feed.json -Force
Remove-Item feed.xml -Force