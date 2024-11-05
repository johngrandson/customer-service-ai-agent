import os

from agents.tools import *
from routines.appointment.policies import *
from routines.general_inquiry.policies import *
from dotenv import load_dotenv
from swarm import Agent

from routines.triage.policies import TRIAGE_INSTRUCTIONS
from routines.appointment.policies import APPOINTMENTS_POLICY, APPOINTMENT_INSTRUCTIONS

load_dotenv()
model = os.getenv("LLM_MODEL", "llama3.2:latest")

def transfer_to_appointments_agent():
    return appointment_agent


def transfer_to_general_inquiry_agent():
    return general_inquiry_agent


def transfer_to_triage():
    """Chame esta função quando um paciente precisar ser transferido para outro agente e um procedimento diferente.
    Por exemplo, se o paciente estiver perguntando sobre um tópico que não é tratado pelo agente atual, chame esta função.
    """
    return triage_agent


def appointment_instructions(context_variables):
    patient_context = context_variables.get("patient_context", None)
    appointment_context = context_variables.get("appointment_context", None)
    return f"""{APPOINTMENTS_POLICY} {APPOINTMENT_INSTRUCTIONS}
    O contexto do paciente é: {patient_context}, e o contexto da consulta é: {appointment_context}"""


triage_agent = Agent(
    name="Agente de Triagem",
    instructions=TRIAGE_INSTRUCTIONS,
    functions=[transfer_to_appointments_agent, transfer_to_general_inquiry_agent],
    model=model,
)

appointment_agent = Agent(
    name="Agente de Agendamento",
    instructions=appointment_instructions,
    functions=[confirm_appointment, reschedule_appointment, get_alternative_dates, check_availability, transfer_to_triage],
    model=model,
)

general_inquiry_agent = Agent(
    name="Atendimento Geral",
    instructions=FAQ_OR_QUESTIONS_POLICY,
    functions=[
        check_dental_plan,
        get_accepted_insurances,
        transfer_to_triage,
    ],
    model=model,
)
