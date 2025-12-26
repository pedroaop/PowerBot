"""
Módulo para gerenciar o menu interativo do bot.
Carrega configurações do menu.json e fornece acesso às ações e mensagens.
"""

import json
import os
from typing import Dict, List, Optional, Tuple


class MenuConfig:
    """Classe para gerenciar configurações do menu."""
    
    def __init__(self, menu_file: str = "menu.json"):
        """
        Inicializa o gerenciador de menu.
        
        Args:
            menu_file: Caminho para o arquivo menu.json
        """
        self.menu_file = menu_file
        self.config = self._load_menu()
        self.actions = self._parse_actions()
        self.cancel_option = self.config.get("cancel_option", "99")
        self.messages = self.config.get("messages", {})
    
    def _load_menu(self) -> Dict:
        """
        Carrega o arquivo menu.json.
        
        Returns:
            Dicionário com as configurações do menu
            
        Raises:
            FileNotFoundError: Se o arquivo menu.json não existir
            json.JSONDecodeError: Se o JSON estiver inválido
        """
        if not os.path.exists(self.menu_file):
            raise FileNotFoundError(
                f"Arquivo {self.menu_file} não encontrado. "
                "Certifique-se de que o arquivo existe na raiz do projeto."
            )
        
        try:
            with open(self.menu_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Erro ao ler {self.menu_file}: JSON inválido. {str(e)}"
            )
    
    def _parse_actions(self) -> Dict[str, Tuple[str, str]]:
        """
        Converte as ações do JSON para o formato usado pelo bot.
        
        Returns:
            Dicionário no formato {id: (description, command)}
        """
        actions = {}
        actions_list = self.config.get("actions", [])
        
        for action in actions_list:
            action_id = action.get("id")
            description = action.get("description")
            command = action.get("command")
            
            if not all([action_id, description, command]):
                raise ValueError(
                    f"Ação inválida no menu.json: cada ação deve ter 'id', "
                    "'description' e 'command'. Ação encontrada: {action}"
                )
            
            actions[action_id] = (description, command)
        
        return actions
    
    def get_action(self, action_id: str) -> Optional[Tuple[str, str]]:
        """
        Obtém uma ação pelo ID.
        
        Args:
            action_id: ID da ação
            
        Returns:
            Tupla (description, command) ou None se não encontrada
        """
        return self.actions.get(action_id)
    
    def get_all_action_ids(self) -> List[str]:
        """
        Retorna lista com todos os IDs de ações.
        
        Returns:
            Lista de IDs
        """
        return list(self.actions.keys())
    
    def get_message(self, key: str, **kwargs) -> str:
        """
        Obtém uma mensagem do template, substituindo placeholders.
        
        Args:
            key: Chave da mensagem
            **kwargs: Valores para substituir nos placeholders
            
        Returns:
            Mensagem formatada
        """
        template = self.messages.get(key, "")
        
        # Substitui placeholders
        for placeholder, value in kwargs.items():
            template = template.replace(f"{{{placeholder}}}", str(value))
        
        return template
    
    def is_cancel_option(self, option: str) -> bool:
        """
        Verifica se uma opção é de cancelamento.
        
        Args:
            option: Opção a verificar
            
        Returns:
            True se for opção de cancelamento
        """
        return option == self.cancel_option
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Valida a estrutura do menu.json.
        
        Returns:
            Tupla (é_válido, lista_de_erros)
        """
        errors = []
        
        # Valida estrutura básica
        if "actions" not in self.config:
            errors.append("Campo 'actions' não encontrado no menu.json")
        
        if "messages" not in self.config:
            errors.append("Campo 'messages' não encontrado no menu.json")
        
        # Valida ações
        if "actions" in self.config:
            actions = self.config["actions"]
            if not isinstance(actions, list):
                errors.append("Campo 'actions' deve ser uma lista")
            else:
                for i, action in enumerate(actions):
                    if not isinstance(action, dict):
                        errors.append(f"Ação {i} não é um objeto válido")
                        continue
                    
                    required_fields = ["id", "description", "command"]
                    for field in required_fields:
                        if field not in action:
                            errors.append(
                                f"Ação {i} (ID: {action.get('id', 'desconhecido')}) "
                                f"não tem o campo '{field}'"
                            )
                    
                    # Valida formato da URL
                    if "command" in action:
                        command = action["command"]
                        if not isinstance(command, str) or not command.startswith("http"):
                            errors.append(
                                f"Ação {i} (ID: {action.get('id', 'desconhecido')}) "
                                "tem um 'command' inválido (deve ser uma URL HTTP/HTTPS)"
                            )
        
        # Valida mensagens
        if "messages" in self.config:
            messages = self.config["messages"]
            if not isinstance(messages, dict):
                errors.append("Campo 'messages' deve ser um objeto")
        
        return len(errors) == 0, errors


# Instância global do menu (será inicializada no main.py)
_menu_config: Optional[MenuConfig] = None


def load_menu(menu_file: str = "menu.json") -> MenuConfig:
    """
    Carrega e valida o menu.
    
    Args:
        menu_file: Caminho para o arquivo menu.json
        
    Returns:
        Instância de MenuConfig
        
    Raises:
        FileNotFoundError: Se o arquivo não existir
        ValueError: Se houver erros de validação
    """
    global _menu_config
    
    _menu_config = MenuConfig(menu_file)
    
    # Valida o menu
    is_valid, errors = _menu_config.validate()
    if not is_valid:
        error_msg = "Erros de validação no menu.json:\n" + "\n".join(f"  - {e}" for e in errors)
        raise ValueError(error_msg)
    
    return _menu_config


def get_menu() -> MenuConfig:
    """
    Retorna a instância do menu carregada.
    
    Returns:
        Instância de MenuConfig
        
    Raises:
        RuntimeError: Se o menu não foi carregado
    """
    if _menu_config is None:
        raise RuntimeError(
            "Menu não foi carregado. Chame load_menu() primeiro."
        )
    return _menu_config

