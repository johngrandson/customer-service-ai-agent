import json

def escalate_to_agent(reason=None):
    return f"Repassando para o atendente: {reason}" if reason else "Repassando para o atendente"

def case_resolved():
    return "Atendimento finalizado. Obrigado."

def check_dental_plan(patient_inquiry):
    """
    Função para realizar a verificação de planos odontológicos e convênios aceitos.
    
    Retorno:
    - Uma mensagem ao paciente com as informações sobre convênios aceitos ou cobertura do tratamento.
    """
    inquiry_type = patient_inquiry.get("type")
    treatment_name = patient_inquiry.get("treatment_name")
    plan_name = patient_inquiry.get("plan_name")
    
    if inquiry_type == "accepted_insurances":
        accepted_insurances = get_accepted_insurances()
        return f"Os convênios aceitos pela clínica são: {', '.join(accepted_insurances)}."
    
    elif inquiry_type == "treatment_coverage" and treatment_name and plan_name:
        coverage_details = get_treatment_coverage(plan_name, treatment_name)
        if coverage_details["is_covered"]:
            co_payment = coverage_details.get("co_payment", "nenhum")
            return f"O tratamento '{treatment_name}' está coberto pelo seu plano '{plan_name}' com coparticipação de {co_payment}."
        else:
            return f"O tratamento '{treatment_name}' não está coberto pelo seu plano '{plan_name}'."
    
    else:
        return escalate_to_agent()

def get_accepted_insurances():
    """
    Função para mostrar a lista de planos odontológicos e convênios aceitos.
    """

    return ["Plano Saúde Brasil", "Unimed", "Amil Dental", "SulÁmerica", "Bradesco Saúde"]

def get_treatment_coverage(plan_name, treatment_name):
    example_coverage_data = {
        "Amil Dental": {"limpeza": {"is_covered": True, "co_payment": "10%"}},
        "Plano Saúde Brasil": {"clareamento": {"is_covered": False}},
        "Unimed": {"extração": {"is_covered": True, "co_payment": "5%"}},
        "SulÁmerica": {"implante": {"is_covered": True, "co_payment": "15%"}},
        "Bradesco Saúde": {"aparelho ortodôntico": {"is_covered": False}}
    }
    return example_coverage_data.get(plan_name, {}).get(treatment_name, {"is_covered": False})

def validate_appointment_details(details):
    """Valida se appointment_details contém os campos necessários."""
    required_fields = ["date", "time", "name", "phone"]
    missing_fields = [field for field in required_fields if field not in details or not details[field]]
    if missing_fields:
        return False, f"Erro: Faltam os seguintes campos obrigatórios: {', '.join(missing_fields)}"
    return True, ""

def confirm_appointment(appointment_details):
    """
    Confirma um agendamento existente com o paciente.
    
    Parâmetros:
    - appointment_details (str ou dict): JSON ou dicionário com data, hora, nome do paciente e telefone.
    
    Retorno:
    - Mensagem de confirmação ou erro com detalhes do agendamento.
    """
    if isinstance(appointment_details, str):
        try:
            appointment_details = json.loads(appointment_details)
        except json.JSONDecodeError:
            return "Erro: Os detalhes do agendamento fornecidos não são válidos. Por favor, envie um JSON válido."

    is_valid, error_message = validate_appointment_details(appointment_details)
    if not is_valid:
        return error_message

    date = appointment_details["date"]
    time = appointment_details["time"]
    name = appointment_details["name"]
    phone = appointment_details["phone"]
    dentist = appointment_details.get("dentist", "qualquer dentista disponível")

    return f"Seu agendamento com o(a) Dr(a). {dentist} está confirmado para {date} às {time}. Nome: {name}, Telefone: {phone}. Se precisar de alguma preparação específica antes da consulta, entraremos em contato."


def reschedule_appointment(current_appointment, new_date, new_time):
    """
    Função para remarcar um agendamento existente.
    Retorno:
    - Uma mensagem ao paciente com a confirmação da remarcação ou alternativas disponíveis.
    """
    if current_appointment:
        dentist = current_appointment.get("dentist")

        is_available = check_availability(dentist, new_date, new_time)
        
        if is_available:
            return f"Seu agendamento com o(a) Dr(a). {dentist} foi remarcado para {new_date} às {new_time}. Aguardamos você!"
        
        else:
            alternative_dates = get_alternative_dates(dentist)
            alternative_text = ", ".join(
                [f"{alt['date']} às {alt['time']}" for alt in alternative_dates]
            )
            return f"O horário solicitado não está disponível. As alternativas disponíveis são: {alternative_text}. Por favor, escolha uma dessas opções ou entre em contato para mais informações."
    
    else:
        return "Não encontramos um agendamento ativo para remarcar. Por favor, peça para agendar uma nova consulta."


def check_availability():
    return True

def get_alternative_dates(dentist=None):
    """
    Retorna uma lista de datas e horários alternativos disponíveis para agendamento.
    
    Parâmetros:
    - dentist (opcional): O nome do dentista, se aplicável.

    Retorno:
    - Uma lista de dicionários, onde cada dicionário contém uma data e um horário.
    """
    return [
        {"date": "10/12/2024", "time": "14:00"},
        {"date": "11/12/2024", "time": "10:00"},
        {"date": "12/12/2024", "time": "16:00"},
        {"date": "13/12/2024", "time": "15:00"},
        {"date": "14/12/2024", "time": "11:00"}
    ]
