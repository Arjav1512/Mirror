const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001'

export const signupUser = async (formData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    })

    const data = await response.json()

    if (!response.ok) {
      return {
        success: false,
        error: data.error || 'Failed to create account'
      }
    }

    return {
      success: true,
      data
    }
  } catch (error) {
    throw new Error(error.message || 'Network error. Please try again.')
  }
}

export const getUser = async (email) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/user/${encodeURIComponent(email)}`)
    const data = await response.json()
    
    if (!response.ok) {
      return null
    }
    
    return data
  } catch (error) {
    console.error('Error fetching user:', error)
    return null
  }
}

