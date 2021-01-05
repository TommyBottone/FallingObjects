using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    public float jumpForce = 20F;
    private float sizeInFeet = 0.5F;
    
    public LayerMask groundLayers;

    public float movementSpeed;
    public Rigidbody2D rb;
    public Transform feet;

    float mx;

    private void Update(){

        mx = Input.GetAxisRaw("Horizontal");

        if(Input.GetButtonDown("Jump") && IsGrounded()){
            Jump();
        }
    }

    private void FixedUpdate(){
        Vector2 movement = new Vector2(mx * movementSpeed, rb.velocity.y);
        rb.velocity = movement;
    }

    void Jump(){
        Vector2 movement = new Vector2(rb.velocity.x, jumpForce);

        rb.velocity = movement;
    }

    public bool IsGrounded(){
        bool retVal = false;
        Collider2D groundCheck = Physics2D.OverlapCircle(feet.position, sizeInFeet, groundLayers);
        if(groundCheck != null)
        {
            retVal = true;   
        }
        return retVal;
    }

}
