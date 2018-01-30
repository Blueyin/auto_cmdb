{% set users = ['name'] %}
{% for user in users %}
{{ user }}:
  user.present:
    - fullname: {{ user }}
    - password: '$1$Pr.UlCBa$P34aOxwq7RjFnnWBTO.CJ/'
    - shell: /bin/bash
    - home: /home/{{ user }}
    - gid: 1002
    - groups:
      - yw
    - require:
      - group: yw

  group.present:
    - gid: 1002
    - name: yw
{% endfor %}
