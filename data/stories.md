## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## buy oxygen
* buy_oxygen
  - oxygen_form
  - form{"name": "oxygen_form"}
  - form{"name": null}

## explain and buy oxygen
* buy_oxygen
  - oxygen_form
  - form{"name": "oxygen_form"}
  - form{"name": null}
* explain_oxygen
  - action_explain_oxygen
  - oxygen_form

## explain difference and buy oxygen
* buy_oxygen
  - oxygen_form
  - form{"name": "oxygen_form"}
  - form{"name": null}
* explain_difference
  - action_explain_difference
  - oxygen_form

## explain concentrator and buy oxygen
* buy_oxygen
  - oxygen_form
  - form{"name": "oxygen_form"}
  - form{"name": null}
* explain_concentrator
  - action_explain_concentrator
  - oxygen_form

## explain tank and buy oxygen
* buy_oxygen
  - oxygen_form
  - form{"name": "oxygen_form"}
  - form{"name": null}
* explain_tank
  - action_explain_tank
  - oxygen_form

## explain why and buy oxygen
* buy_oxygen
  - oxygen_form
  - form{"name": "oxygen_form"}
  - form{"name": null}
* explain_why
  - action_explain_why
  - oxygen_form

## explain size and buy oxygen
* buy_oxygen
  - oxygen_form
  - form{"name": "oxygen_form"}
  - form{"name": null}
* explain_size
  - action_explain_size
  - oxygen_form

## explain everything and buy oxygen
* buy_oxygen
  - oxygen_form
  - form{"name": "oxygen_form"}
  - form{"name": null}
* explain_oxygen
  - action_explain_oxygen
  - oxygen_form
* explain_why
  - action_explain_why
  - oxygen_form
* explain_difference
  - action_explain_difference
  - oxygen_form
* explain_size
  - action_explain_size
  - oxygen_form
