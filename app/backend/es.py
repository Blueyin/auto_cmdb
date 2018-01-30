#!/usr/bin/python
import elasticsearch
import datetime
import sys
import json
reload(sys)
import MySQLdb
sys.setdefaultencoding("utf8")
from elasticsearch import Elasticsearch


class ES_SEARCH(object):
    def __init__(self,start,end,samples):
        self.start = start
        self.end = end
        self.samples = samples
    def es_search(self):
        es = Elasticsearch([{'host':'192.168.0.3','port':9200}])
        if not self.start:
            self.start = "2017-09-10T17:45:54.736"
        if not self.end:
            self.end = self.start
        query_json = {
            "from": 0,
            "size": 0,
            "query": {
                "bool": {
                    "filter": {
                        "bool": {
                            "must": {
                                "bool": {
                                    "must": [
                                        {
                                            "range": {
                                                "ts_min": {
                                                    "from": self.start,
                                                    "to": None,
                                                    "include_lower": True,
                                                    "include_upper": True
                                                }
                                            }
                                        },
                                        {
                                            "range": {
                                                "ts_min": {
                                                    "from": None,
                                                    "to": self.end,
                                                    "include_lower": True,
                                                    "include_upper": True
                                                }
                                            }
                                        },
                                        {
                                            "wildcard": {
                                                "sample": self.samples
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            },
            "_source": {
                "includes": [
                    "sample",
                    "SUM",
                    "SUM",
                    "AVG",
                    "logstash_checksum"
                ],
                "excludes": []
            },
            "fields": [
                "sample",
                "logstash_checksum"
            ],
            "aggregations": {
                "logstash_checksum": {
                    "terms": {
                        "field": "logstash_checksum",
                        "size": 200
                    },
                    "aggregations": {
                        "sample": {
                            "terms": {
                                "field": "sample",
                                "size": 0,
                                "order": {
                                    "cnt_sum": "desc"
                                }
                            },
                            "aggregations": {
                                "query_time_sum": {
                                    "sum": {
                                        "field": "query_time_sum"
                                    }
                                },
                                "cnt_sum": {
                                    "sum": {
                                        "field": "ts_cnt"
                                    }
                                },
                                "query_time_avg": {
                                    "avg": {
                                        "field": "query_time_sum"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        res = es.search(body=query_json)
        ret = []
        #print res["aggregations"]
        for sample in res["aggregations"]["logstash_checksum"]["buckets"]:
            ret.append(sample)
        try: 
            rets=ES_SEARCH.result(self, ret)
	except:
            return 'Faild to searh!'
        else:
            return rets
    def result(self,r_data):
        rets = []
        reta = []
        retb = []
        retc = []
        retd = []
        rete = []
        #retes = []
        result_data = list()
        for ret in r_data:
	    for key,value in ret.items():
		if key=="key":
		    reta.append(value)
		    #print value
		elif key=="sample":
            	#for res in ret['sample']['buckets']:
                    for k in value["buckets"]:
                        for n, m in k.items():
                            if n == "cnt_sum":
                                m = m['value']
                                retb.append(m)
                            elif n == "query_time_avg":
                                m = m['value']
                                retc.append(m)
                            elif n == "query_time_sum":
                                m = m['value']
                                retd.append(m)
                            elif n == "key":
                                rete.append(m)
        for i in range(len(reta)):
            values = (reta[i], retb[i], retc[i], retd[i], rete[i])
            result_data.append(values)
        conn = MySQLdb.connect(host="192.168.0.2", user="test", passwd="test_1234", db="cmdb", charset="utf8")
        cursor = conn.cursor()
	sql_del = '''DELETE FROM `app_search_return`'''
        sql = '''INSERT INTO `app_search_return`
                (`logstash_checksum`, `cnt_sum`, `query_time_avg`, `query_time_sum`,  `samples` )
                VALUES ( %s, %s, %s, %s, %s)'''
	try: 
            cursor.execute(sql_del)
            cursor.executemany(sql,result_data)
            cursor.execute("COMMIT")
	except:
	    db.rollback()
	    return 'false'
	else:
            conn.close()
            return 'OK'

if __name__ == "__main__":
    start = sys.argv[1]
    end = sys.argv[2]
    samples= "*residential_building_house_no*"
    search=ES_SEARCH(start,end,samples)
    print search.es_search()
