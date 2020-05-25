# Melnor Raincloud

#### Instructions on how to integrate your Melnor Raincloud sprinkler system within Home Assistant.

---

![HACS Validation](https://github.com/vanstinator/hass-raincloud/workflows/HACS%20Validation/badge.svg?branch=master) ![Hassfest Validation](https://github.com/vanstinator/hass-raincloud/workflows/Hassfest%20Validation/badge.svg?branch=master)

<!-- ### Stats
![GitHub All Releases](https://img.shields.io/github/downloads/vanstinator/hass-raincloud/total?color=orange&label=Total%20downloads&style=for-the-badge) -->

##### Stable
![GitHub release (latest by date)](https://img.shields.io/github/v/release/vanstinator/hass-raincloud?style=for-the-badge) ![GitHub Release Date](https://img.shields.io/github/release-date/vanstinator/hass-raincloud?style=for-the-badge) ![GitHub Releases](https://img.shields.io/github/downloads/vanstinator/hass-raincloud/latest/total?color=purple&label=%20release%20Downloads&style=for-the-badge) 

---

The `raincloud` integration allows you to integrate your [Melnor RainCloud](https://wifiaquatimer.com) sprinkler system in Home Assistant.

## Installation
The easiest way to install and stay updated with this integration is through the Home Assistant Community Store (HACS)

1. Install HACS https://hacs.xyz/docs/installation/prerequisites
1. Configure HACS https://hacs.xyz/docs/configuration/start
1. Add a custom repo in HACS using this url `https://github.com/vanstinator/hass-raincloud`
1. On your `Integrations` page in HACS you should now see a card for `Melnor Raincloud` Click `Install`. Reboot Home Assistant`.

## Configuration

To enable it the component add the following to your `configuration.yaml` file:

Parameter | Required | Type | Description
------------ | ------------- | ------------ | ------------- |
username | true | string | The username for accessing your Melnor RainCloud account
password | true | string | The password for accessing your Melnor RainCloud account

```yaml
# Example configuration.yaml entry
raincloud:
  username: YOUR_USERNAME
  password: YOUR_PASSWORD
```

## Binary Sensor

Once you have enabled the [Raincloud component](#configuration), add the following to your `configuration.yaml` file:

##### Monitored Conditions
Parameter | Default | Type | Description
------------ | ------------- |------------ | ------------- |
is_watering | true | boolean | Currently watering per zone
status | true | string | Status from the Melnor RainCloud Controller and Melnor RainCloud Faucet

```yaml
# Example configuration.yaml entry
binary_sensor:
  - platform: raincloud
    # These properties are optional. All are enabled by default
    # monitored_conditions:
    #   - is_watering
    #   - status
```

## Sensor

Once you have enabled the [Raincloud component](#configuration), add the following to your `configuration.yaml` file:

##### Monitored Conditions

Parameter | Description
------------ | ------------- |
battery | Battery level of the Melnor RainCloud faucet
next_cycle | Next schedule for the watering cycle per zone
rain_delay | Number of days the automatic watering will be delayed due to raining per zone
watering_time | Watering minutes remaining per zone


```yaml
# Example configuration.yaml entry
sensor:
  - platform: raincloud
    # These properties are optional. All are enabled by default
    # monitored_conditions:
    #   - battery
    #   - next_cycle
    #   - rain_delay
    #   - watering_time
```

## Switch

Once you have enabled the [Raincloud component](#configuration), add the following to your `configuration.yaml` file:

##### Monitored Conditions

Parameter | Description
------------ | ------------- |
auto_watering | Toggle the watering scheduled per zone
manual_watering | Toggle manually the watering per zone. It will inherent the value in minutes specified in `watering_minutes`

```yaml
# Example configuration.yaml entry
switch:
  - platform: raincloud
    # Default is 15 minutes. Allowed values are 5, 10, 15, 30, 45, 60
    # watering_minutes: 60
    # These properties are optional. All are enabled by default
    # monitored_conditions:
    #  - auto_watering
    #  - manual_watering
```
