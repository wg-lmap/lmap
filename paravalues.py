#!/bin/python
# -*- coding: UTF-8 -*-

#pre configuration
pre_conf='''
{
  "ma-config": {
    "ma-agent-id": "550e8400-e29b-41d4-a716-446655440000",
    "ma-control-tasks": [
      {
        "ma-task-name": "Controller configuration",
        "ma-task-registry-entry": "urn:ietf:lmap:control:http_controller_configuration"
      }
    ],
    "ma-control-channels": [
      {
        "ma-channel-name": "Controller channel",
        "ma-channel-target": "http://www.example.com/lmap/controller",
        "ma-channel-credientials": { } 
      }
    ],
    "ma-control-schedules": [
      {
        "ma-schedule-name": "pre-configured schedule",
        "ma-schedule-tasks": {
          
            "ma-schedule-task-name": "Controller configuration",
            "ma-schedule-channels": [
              {
                "ma-schedule-channel-interface-selection": [1],
                "ma-schedule-task-source-channel-names": ["Controller channel"]
              }
            ]
          
        },
        "ma-schedule-timing": {
          "ma-timing-name": "startup plus up to one hour",
          "ma-timing-startup": {
          },
          "ma-timing-random-spread": "3600000"
        }
      }
    ],
    "ma-credentials": { }
  }
}'''

#config
conf='''
{
  "ma-config": {
    "ma-agent-id": "550e8400-e29b-41d4-a716-446655440000",
    "ma-control-tasks": [
      {
        "ma-task-name": "Controller configuration",
        "ma-task-registry-entry": "urn:ietf:lmap:control:http_controller_configuration"
      },
      {
        "ma-task-name": "Controller status and capabilities",
        "ma-task-registry-entry": "urn:ietf:lmap:control:http_controller_status_and_capabilities"
      },
      {
        "ma-task-name": "Controller instruction",
        "ma-task-registry-entry": "urn:ietf:lmap:control:http_controller_instruction"
      }
    ],
    "ma-control-channels": [
      {
        "ma-channel-name": "Controller instruction",
        "ma-channel-target": "http://www.example.com/lmap/controller",
        "ma-channel-credientials": { } 
      }
    ],
    "ma-control-schedules": [
      {
        "ma-schedule-name": "Controller schedule",
        "ma-schedule-tasks": [
          {
            "ma-schedule-task-name": "Controller configuration",
            "ma-schedule-channels": [
              {
                "ma-schedule-channel-interface-selection": [1],
                "ma-schedule-task-source-channel-names": ["Controller channel"]
              }
            ]
          },
          {
            "ma-schedule-task-name": "Controller status and capabilities",
            "ma-schedule-channels": [
              {
                "ma-schedule-channel-interface-selection": [1],
                "ma-schedule-task-source-channel-names": ["Controller channel"]
              }
            ]
          },
          {
            "ma-schedule-task-name": "Controller instruction",
            "ma-schedule-channels": [
              {
                "ma-schedule-channel-interface-selection": [1],
                "ma-schedule-task-source-channel-names": ["Controller channel"]
              }
            ]
          }
        ],
        "ma-schedule-timing": {
          "ma-timing-name": "hourly randomly",
          "ma-timing-calendar": {
            "ma-calendar-minutes": ["00"],
            "ma-calendar-seconds": ["00"]
          },
          "ma-timing-random-spread": "3600000"
        }
      }
    ],
    "ma-credentials": { }
  }
}'''
#stat and cap
stat_and_cap='''
{
  "ma-status-and-capabilities": {
    "ma-agent-id": "550e8400-e29b-41d4-a716-446655440000",
    "ma-device-id": "urn:dev:mac:0024befffe804ff1",
    "ma-hardware": "mfr-home-gateway-v10",
    "ma-firmware": "25637748-rev2a",
    "ma-version": "ispa-v1.01",
    "ma-interfaces": [
      {
        "ma-interface-name": "broadband",
        "ma-interface-type": "PPPoE"
      }
    ],
    "ma-last-measurement": "",
    "ma-last-report": "",
    "ma-last-instruction": "",
    "ma-last-configuration": "2014-06-08T22:47:31+00:00",
    "ma-supported-tasks": [
      {
        "ma-task-name": "Controller configuration",
        "ma-task-registry": "urn:ietf:lmap:control:http_controller_configuration"
      },,
      {
        "ma-task-name": "Controller status and capabilities",
        "ma-task-registry": "urn:ietf:lmap:control:http_controller_status_and_capabilities"
      },
      {
        "ma-task-name": "Controller instruction",
        "ma-task-registry": "urn:ietf:lmap:control:http_controller_instruction"
      },
      {
        "ma-task-name": "Report",
        "ma-task-registry": "urn:ietf:lmap:report:http_report"
      },
      {
        "ma-task-name": "UDP Latency",
        "ma-task-registry": "urn:ietf:ippm:measurement:UDPLatency-Poisson-XthPercentileMean"
      }
    ]
  }
}'''

#instruction   destination-ip、ma-channel-target是今后修改的参数
ins= '''
{
  "ma-instruction": {
    "ma-instruction-tasks": [
      {
        "ma-task-name": "ping",
        "ma-task-registry-entry": "urn:ietf:ippm:measurement:ping",
        "ma-task-options": [
          {"name": "X", "value": "99"},
          {"name":"rate", "value": "5"},
          {"name":"destination-ip", "value": {"version":"ipv4", "ip-address":"127.0.0.1"}}
        ],
        "ma-task-suppress-by-default": "TRUE"
      },
      {
        "ma-task-name": "Report",
        "ma-task-registry-entry": "urn:ietf:lmap:report:http_report",
        "ma-task-options": [
          {"name": "report-with-no-data", "value": "FALSE"}
        ],
        "ma-task-suppress-by-default": "FALSE"
      }
    ],
    "ma-report-channels": [
      {
        "ma-channel-name": "Collector A",
        "ma-channel-target": "http://127.0.0.1:8088/ma/rep",
        "ma-channel-credientials": { } 
      }
    ],
    "ma-instruction-schedules": [
      {
        "ma-schedule-name": "4 times daily test UDP latency and report",
        "ma-schedule-tasks": [
          {
            "ma-schedule-task-name": "ping",
            "ma-schedule-downstream-tasks": [
              {
                "ma-schedule-task-output-selection": [1],
                "ma-schedule-task-downstream-task-configuration-names": "Report"
              }
            ]
          },
          {
            "ma-schedule-task-name": "Report",
            "ma-schedule-channels": [
              {
                "ma-schedule-channel-interface-selection": [1],
                "ma-schedule-channel-names": "Collector A"
              }
            ]
          }
        ],
  
        "ma-schedule-timing": {
          "ma-timing-name": "once every 6 hours",
          "ma-timing-calendar": {
            "ma-calendar-hours": ["17"],
            "ma-calendar-minutes": ["00"],
            "ma-calendar-seconds": ["00","10","20"]
          },
          "ma-timing-random-spread": "21600000"
        }
      }
    ]
  }
}'''
#report
rep={
  "ma-report": {
    "ma-report-date": "2014-06-09T02:30:45+00:00",
    "ma-report-agent-id": "550e8400-e29b-41d4-a716-446655440000",
    "ma-report-tasks": [ 
    	{
      "ma-report-task-config": {
        "ma-task-name": "UDP Latency",
        "ma-task-registry-entry": "urn:ietf:ippm:measurement:UDPLatency-Poisson-XthPercentileMean",
        "ma-task-options": [
          {"name": "X", "value": "99"},
          {"name":"rate", "value": "5"},
          {"name":"duration", "value": "30.000"},
          {"name":"interface", "value": "broadband"},
          {"name":"destination-ip", "value": {"version":"ipv4", "ip-address":"192.168.2.54"}},
          {"name":"destination-port", "value": "50000"},
          {"name":"source-port", "value": "50000"}
        ]
      },
      "ma-report-task-column-labels": ["start-time", "cross-traffic","ipaddr"],
      "ma-report-task-rows": ["2014-06-09T02:30:10+00:00", "24.1","127.0.0.1"]
    }
   ]
  }
}
# Suppression
sup='''
   {
     "ma-instruction": {
       "ma-suppression": {
          "ma-suppression-enabled": "TRUE"
       }
     }
   }'''
# exit
exit_ins='''
   {
     "ma-instruction": {
       "ma-exit": {
          "ma-exit-enabled": "TRUE"
       }
     }
   }'''

