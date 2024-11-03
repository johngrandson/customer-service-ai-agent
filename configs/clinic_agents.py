from configs.tools import *
from routines.appointment.policies import *
from routines.general_inquiry.policies import *
from routines.prompts import STARTER_PROMPT

from swarm import Agent


def transfer_to_appointments_agent():
    return appointment_agent


def transfer_to_general_inquiry_agent():
    return general_inquiry_agent


def transfer_to_triage():
    """Chame esta função quando um paciente precisar ser transferido para outro agente e um procedimento diferente.
    Por exemplo, se o paciente estiver perguntando sobre um tópico que não é tratado pelo agente atual, chame esta função.
    """
    return triage_agent


def triage_instructions(context_variables):
    patient_context = context_variables.get("patient_context", None)
    appointment_context = context_variables.get("appointment_context", None)
    return f"""Você está realizando a triagem de pedidos de pacientes e deve transferir para a intenção correta sem detalhar seus pensamentos para o paciente.
    Seja direto, pergunte informações necessárias e responda com clareza em português.
    {STARTER_PROMPT}
    Quando precisar de mais informações para direcionar o pedido a um agente, faça uma pergunta direta sem explicar por que está perguntando.
    Não compartilhe seu processo de pensamento com o paciente! Não faça suposições não razoáveis em nome do paciente.
    O contexto do paciente é: {patient_context}, e o contexto da consulta é: {appointment_context}
    """


triage_agent = Agent(
    name="Agente de Triagem",
    instructions=triage_instructions,
    functions=[transfer_to_appointments_agent, transfer_to_general_inquiry_agent, case_resolved],
)

appointment_agent = Agent(
    name="Agente de Agendamento",
    instructions=APPOINTMENTS_POLICY,
    functions=[confirm_appointment, reschedule_appointment, get_alternative_dates, check_availability, transfer_to_triage, transfer_to_general_inquiry_agent],
    parallel_tool_calls=False,
)

general_inquiry_agent = Agent(
    name="Atendimento Geral",
    instructions=FAQ_OR_QUESTIONS_POLICY,
    functions=[
        check_dental_plan,
        get_accepted_insurances,
        transfer_to_triage,
        transfer_to_appointments_agent
    ],
)
