{% set users = ['name'] %}
{% for user in users %}
{{ user }}:
  user.present:
    - fullname: {{ user }}
    - password: '$1$Pr.UlCBa$P34aOxwq7RjFnnWBTO.CJ/'
    - shell: /bin/bash
    - home: /home/{{ user }}
    - gid: 1003
    - groups:
      - dev
    - require:
      - group: dev

  group.present:
    - gid: 1003
    - name: dev
{% endfor %}
