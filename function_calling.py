
decision_function = {
    "name": "decide_action",
    "description": "Decide si el usuario quiere generar o editar una imagen, o si no es necesario realizar una acción auxiliar.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "La acción a realizar: 'generate', 'edit', o 'none'.",
                "enum": ["generate", "edit", "none"]
            }
        },
        "required": ["action"]
    }
}


generate_image_function = {
    "name": "generate_image",
    "description": "Generar una imagen basada en los parámetros proporcionados.",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "La descripción de la imagen a generar.",
            },
            "aspect_ratio": {
                "type": "string",
                "description": "La proporción de aspecto de la imagen. No puede usarse junto con resolución.",
                "enum": [
                    "ASPECT_10_16", "ASPECT_16_10", "ASPECT_9_16", 
                    "ASPECT_16_9", "ASPECT_3_2", "ASPECT_2_3", 
                    "ASPECT_4_3", "ASPECT_3_4", "ASPECT_1_1", 
                    "ASPECT_1_3", "ASPECT_3_1"
                ]
            },
            "model": {
                "type": "string",
                "description": "El modelo utilizado para generar la imagen.",
                "enum": ["V_1", "V_1_TURBO", "V_2", "V_2_TURBO"]
            },
            "magic_prompt_option": {
                "type": "string",
                "description": "Determina si se debe usar MagicPrompt en la generación.",
                "enum": ["AUTO", "ON", "OFF"]
            },
            "seed": {
                "type": "integer",
                "description": "La semilla para la generación de la imagen. Valores permitidos entre 0 y 2147483647.",
                "minimum": 0,
                "maximum": 2147483647
            },
            "style_type": {
                "type": "string",
                "description": "El estilo de generación de la imagen. Solo aplicable a modelos V_2 y superiores.",
                "enum": ["AUTO", "GENERAL", "REALISTIC", "DESIGN", "RENDER_3D", "ANIME"]
            },
            "negative_prompt": {
                "type": "string",
                "description": "Descripción de lo que se debe excluir de la imagen. Tiene menor prioridad que las descripciones del prompt principal."
            },
            "resolution": {
                "type": "string",
                "description": "La resolución para generar la imagen. No puede usarse junto con aspecto de relación.",
                "enum": [
                    "RESOLUTION_512_1536", "RESOLUTION_576_1408", "RESOLUTION_576_1472",
                    "RESOLUTION_576_1536", "RESOLUTION_640_1024", "RESOLUTION_640_1344",
                    "RESOLUTION_640_1408", "RESOLUTION_640_1472", "RESOLUTION_640_1536",
                    "RESOLUTION_704_1152", "RESOLUTION_704_1216", "RESOLUTION_704_1280",
                    "RESOLUTION_704_1344", "RESOLUTION_704_1408", "RESOLUTION_704_1472",
                    "RESOLUTION_720_1280", "RESOLUTION_736_1312", "RESOLUTION_768_1024",
                    "RESOLUTION_768_1088", "RESOLUTION_768_1152", "RESOLUTION_768_1216",
                    "RESOLUTION_768_1232", "RESOLUTION_768_1280", "RESOLUTION_768_1344",
                    "RESOLUTION_832_960", "RESOLUTION_832_1024", "RESOLUTION_832_1088",
                    "RESOLUTION_832_1152", "RESOLUTION_832_1216", "RESOLUTION_832_1248",
                    "RESOLUTION_864_1152", "RESOLUTION_896_960", "RESOLUTION_896_1024",
                    "RESOLUTION_896_1088", "RESOLUTION_896_1120", "RESOLUTION_896_1152",
                    "RESOLUTION_960_832", "RESOLUTION_960_896", "RESOLUTION_960_1024",
                    "RESOLUTION_960_1088", "RESOLUTION_1024_640", "RESOLUTION_1024_768",
                    "RESOLUTION_1024_832", "RESOLUTION_1024_896", "RESOLUTION_1024_960",
                    "RESOLUTION_1024_1024", "RESOLUTION_1088_768", "RESOLUTION_1088_832",
                    "RESOLUTION_1088_896", "RESOLUTION_1088_960", "RESOLUTION_1120_896",
                    "RESOLUTION_1152_704", "RESOLUTION_1152_768", "RESOLUTION_1152_832",
                    "RESOLUTION_1152_864", "RESOLUTION_1152_896", "RESOLUTION_1216_704",
                    "RESOLUTION_1216_768", "RESOLUTION_1216_832", "RESOLUTION_1232_768",
                    "RESOLUTION_1248_832", "RESOLUTION_1280_704", "RESOLUTION_1280_720",
                    "RESOLUTION_1280_768", "RESOLUTION_1280_800", "RESOLUTION_1312_736",
                    "RESOLUTION_1344_640", "RESOLUTION_1344_704", "RESOLUTION_1344_768",
                    "RESOLUTION_1408_576", "RESOLUTION_1408_640", "RESOLUTION_1408_704",
                    "RESOLUTION_1472_576", "RESOLUTION_1472_640", "RESOLUTION_1472_704",
                    "RESOLUTION_1536_512", "RESOLUTION_1536_576", "RESOLUTION_1536_640"
                ]
            },
            "color_palette": {
                "type": "object",
                "description": "Una paleta de colores para la generación, ya sea mediante un preset o hexadecimales explícitos.",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Un preset de paleta de colores.",
                        "enum": ["EMBER", "FRESH", "JUNGLE", "MAGIC", "MELON", "MOSAIC", "PASTEL", "ULTRAMARINE"]
                    },
                    "members": {
                        "type": "array",
                        "description": "Lista de colores hexadecimales para definir la paleta.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "color_hex": {
                                    "type": "string",
                                    "description": "Código hexadecimal del color.",
                                    "pattern": "^#(?:[0-9a-fA-F]{3}){1,2}$"
                                },
                                "color_weight": {
                                    "type": "number",
                                    "description": "Peso del color en la paleta, entre 0.05 y 1.0.",
                                    "minimum": 0.05,
                                    "maximum": 1.0
                                }
                            },
                            "required": ["color_hex"]
                        }
                    }
                },
                "anyOf": [
                    {"required": ["name"]},
                    {"required": ["members"]}
                ]
            }
        },
        "required": ["prompt"]
    },
}


# Aqui se esta usando la url en lugar del archivo
edit_image_function = {
    "name": "edit_image",
    "description": "Edita una imagen utilizando una URL de imagen, una máscara generada automáticamente y otros parámetros opcionales.",
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "Descripción del resultado esperado después de la edición."
            },
            "model": {
                "type": "string",
                "description": "El modelo utilizado para editar la imagen, si se pide algo especifico usar V_2_TURBO.",
                "enum": ["V_2", "V_2_TURBO"] #Unicamente funciona para v_2 o v_2 turbo la edicion de imagenes
            },
            "magic_prompt_option": {
                "type": "string",
                "description": "Determina si MagicPrompt debe ser utilizado durante la edición para obtener un mejor resultado.",
                "enum": ["AUTO", "ON", "OFF"]
            },
            "seed": {
                "type": "integer",
                "description": "Semilla para la generación de la imagen editada.",
                "minimum": 0,
                "maximum": 2147483647
            },
            "style_type": {
                "type": "string",
                "description": "Estilo visual para la edición teniendo en cuenta el contexto anterior.",
                "enum": ["AUTO", "GENERAL", "REALISTIC", "DESIGN", "RENDER_3D", "ANIME"]
            },
            "image_url": {
                "type": "string",
                "description": "URL de la imagen original (JPEG, PNG o WEBP)."
            }
        },
        "required": ["prompt", "model", "image_url"]
    },
}
