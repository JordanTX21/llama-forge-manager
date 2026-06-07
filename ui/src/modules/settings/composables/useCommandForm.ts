import { useForm } from 'vee-validate'
import * as yup from 'yup'
import type { CommandConfig } from '../services/settings.service'

const validationSchema = yup.object({
  filename: yup.string().required('Filename is required'),
  alias: yup.string().required('Alias is required'),
  model_path: yup.string(),
  mmproj_path: yup.string().nullable(),
  ctx_size: yup.number().integer().default(4096),
  ngl: yup.number().integer().default(35),
  port: yup.number().integer().default(8080),
  flash_attention: yup.boolean().default(true),
  thinking_mode: yup.boolean().default(false),
  
  threads: yup.number().integer().default(-1),
  threads_batch: yup.number().integer().default(-1),
  np: yup.number().integer().default(-1),
  cr: yup.string().default('').nullable(),
  crb: yup.string().default('').nullable(),
  cpu_strict: yup.boolean().default(false),
  cpu_strict_batch: yup.boolean().default(false),

  batch_size: yup.number().integer().default(-1),
  ubatch_size: yup.number().integer().default(-1),
  prio: yup.number().integer().default(-1),
  prio_batch: yup.number().integer().default(-1),
  poll: yup.number().integer().default(-1),
  poll_batch: yup.number().integer().default(-1),

  cache_type_k: yup.string().default('q8_0'),
  cache_type_v: yup.string().default('q8_0'),
  kv_unified: yup.boolean().default(false),
  no_mmap: yup.boolean().default(false),
  mlock: yup.boolean().default(false),

  ncmoe: yup.number().integer().default(-1),
  spec_type: yup.string().default('').nullable(),
  spec_draft_n_max: yup.number().integer().default(-1),

  temp: yup.number().default(0.6),
  top_p: yup.number().default(0.95),
  top_k: yup.number().integer().default(20),
  min_p: yup.number().default(0.0),
  presence_penalty: yup.number().default(0.0),
  repeat_penalty: yup.number().default(1.0),

  jinja: yup.boolean().default(false),
  raw_content: yup.string().default('').nullable()
})

export const useCommandForm = () => {
  return useForm<CommandConfig>({
    validationSchema,
    initialValues: {
      filename: '',
      alias: '',
      model_path: '',
      mmproj_path: '',
      ctx_size: 4096,
      ngl: 35,
      port: 8080,
      flash_attention: false,
      thinking_mode: false,
      threads: -1,
      threads_batch: -1,
      np: -1,
      cr: '',
      crb: '',
      cpu_strict: false,
      cpu_strict_batch: false,
      batch_size: -1,
      ubatch_size: -1,
      prio: -1,
      prio_batch: -1,
      poll: -1,
      poll_batch: -1,
      cache_type_k: 'q8_0',
      cache_type_v: 'q8_0',
      kv_unified: false,
      no_mmap: false,
      mlock: false,
      ncmoe: -1,
      spec_type: '',
      spec_draft_n_max: -1,
      temp: 0.6,
      top_p: 0.95,
      top_k: 20,
      min_p: 0.0,
      presence_penalty: 0.0,
      repeat_penalty: 1.0,
      jinja: false,
      raw_content: ''
    }
  })
}
