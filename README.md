# dragalia-site-back

[![back-deployment]][back-site]
[![back-site-status]][back-site]
[![back-ci]][back-ci-link]
[![back-cq-badge]][back-cq-link]
[![back-lgtm-alert-badge]][back-lgtm-alert-link]
[![back-lgtm-quality-badge]][back-lgtm-quality-link]
[![back-time-badge]][back-time-link]

Backend of [Dragalia Lost info website by OM][site].

## Environment Variables

Name | Required/Optional | Description
:---: | :---: | :---:
MONGO_URL | Required | Connection string of MongoDB database.
MONGO_DB | Optional | Database to use. If specified, all data will be manipulated in the given database only.
TEST | Optional | Specify this to `1` for CI test-specific behavior.

[site]: https://dl.raenonx.cc

[back-deployment]: https://pyheroku-badge.herokuapp.com/?app=dragalia-site-back&style=flat-square

[back-site]: https://dl-back.raenonx.cc

[back-site-status]: https://img.shields.io/website?down_message=offline&up_message=online&url=https%3A%2F%2Fdl-back.raenonx.cc

[back-cq-link]: https://www.codacy.com/gh/RaenonX-DL/dragalia-site-back/dashboard

[back-cq-badge]: https://app.codacy.com/project/badge/Grade/8710325ebb8049c18a5576aa2feb8567

[back-ci]: https://github.com/RaenonX-DL/dragalia-site-back/workflows/Python%20CI/badge.svg

[back-ci-link]: https://github.com/RaenonX-DL/dragalia-site-back/actions?query=workflow%3A%22Python+CI%22

[back-time-link]: https://wakatime.com/badge/github/RaenonX-DL/dragalia-site-back

[back-time-badge]: https://wakatime.com/badge/github/RaenonX-DL/dragalia-site-back.svg

[back-lgtm-alert-badge]: https://img.shields.io/lgtm/alerts/g/RaenonX-DL/dragalia-site-back.svg?logo=lgtm&logoWidth=18

[back-lgtm-alert-link]: https://lgtm.com/projects/g/RaenonX-DL/dragalia-site-back/alerts/

[back-lgtm-quality-badge]: https://img.shields.io/lgtm/grade/python/g/RaenonX-DL/dragalia-site-back.svg?logo=lgtm&logoWidth=18

[back-lgtm-quality-link]: https://lgtm.com/projects/g/RaenonX-DL/dragalia-site-back/context:python
