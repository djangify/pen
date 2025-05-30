# core/views.py
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from blog.models import Post
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import subprocess
import logging

logger = logging.getLogger(__name__)


def home_view(request):
    # Get the latest 3 published blog posts
    latest_posts = Post.objects.filter(
        status="published", publish_date__lte=timezone.now()
    ).order_by("-publish_date")[:3]

    context = {
        "latest_posts": latest_posts,
    }

    return render(request, "index.html", context)


def about(request):
    """
    View for the About page
    """
    context = {
        "title": "About Pen and I Publishing",
        "meta_description": "Learn about Pen and I Publishing and our mission to help everyone capture their life stories and memories.",
    }
    return render(request, "core/about.html", context)


def notebook(request):
    """
    View for the Notebook page
    """
    context = {
        "title": "Paperback Notebooks by Pen & I Publishing",
        "meta_description": "We create lined paperback notebooks to help you capture your life stories and memories.",
    }
    return render(request, "core/paperback_notebook.html", context)


def policies_index(request):
    """
    View for the index of policies page
    """
    breadcrumbs = [{"title": "Policies", "url": None}]

    context = {
        "title": "Index of all Policies for Pen & I Publishing",
        "meta_description": "This is the most up to date index of all policies for our website.",
        "breadcrumbs": breadcrumbs,
    }
    return render(request, "policy/policies_index.html", context)


def privacy_policy(request):
    """
    View for the privacy policy page
    """
    breadcrumbs = [
        {"title": "Policies", "url": reverse("core:policies_index")},
        {"title": "Privacy Policy", "url": None},
    ]

    context = {
        "title": "Privacy Policy for Pen & I Publishing",
        "meta_description": "This is the most up to date privacy policy for our website",
        "breadcrumbs": breadcrumbs,
    }
    return render(request, "policy/privacy_policy.html", context)


def terms_conditions(request):
    """
    View for the terms and conditions policy page
    """
    breadcrumbs = [
        {"title": "Policies", "url": reverse("core:policies_index")},
        {"title": "Terms & Conditions", "url": None},
    ]

    context = {
        "title": "Terms and Conditions Policy for Pen & I Publishing",
        "meta_description": "This is the most up to date terms and conditions policy for our website",
        "breadcrumbs": breadcrumbs,
    }
    return render(request, "policy/terms_conditions.html", context)


def advertising_policy(request):
    """
    View for the advertising policy page
    """
    breadcrumbs = [
        {"title": "Policies", "url": reverse("core:policies_index")},
        {"title": "Advertising Policy", "url": None},
    ]

    context = {
        "title": "Advertising Policy for Pen & I Publishing",
        "meta_description": "This is the most up to date advertising policy for our website",
        "breadcrumbs": breadcrumbs,
    }
    return render(request, "policy/advertising_policy.html", context)


def support_policy(request):
    """
    View for the help and support policy page
    """
    breadcrumbs = [
        {"title": "Policies", "url": reverse("core:policies_index")},
        {"title": "Help & Support", "url": None},
    ]

    context = {
        "title": "Help and Support Policy for Pen & I Publishing",
        "meta_description": "This is the most up to date help and support policy for our website",
        "breadcrumbs": breadcrumbs,
    }
    return render(request, "policy/support_policy.html", context)


def cookies_policy(request):
    """
    View for the cookies policy page
    """
    breadcrumbs = [
        {"title": "Policies", "url": reverse("core:policies_index")},
        {"title": "Cookies Policy", "url": None},
    ]

    context = {
        "title": "Cookies Policy for Pen & I Publishing",
        "meta_description": "This is the most up to date cookies policy for our website",
        "breadcrumbs": breadcrumbs,
    }
    return render(request, "policy/cookies_policy.html", context)


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@csrf_exempt
@require_POST
def webhook_handler(request):
    import hashlib
    import hmac
    import os

    try:
        # Log the webhook received
        logger.info("Webhook received from GitHub")
        logger.info(f"Content-Type: {request.content_type}")

        # Get the webhook secret from environment
        webhook_secret = os.environ.get("GITHUB_WEBHOOK_SECRET")

        if not webhook_secret:
            logger.error("GITHUB_WEBHOOK_SECRET not set in environment")
            return HttpResponse("Webhook secret not configured", status=500)

        # Get GitHub signature
        github_signature = request.headers.get("X-Hub-Signature-256", "")

        if github_signature:
            # Calculate expected signature using the raw body
            expected_signature = (
                "sha256="
                + hmac.new(
                    webhook_secret.encode("utf-8"), request.body, hashlib.sha256
                ).hexdigest()
            )

            # Compare signatures
            if not hmac.compare_digest(github_signature, expected_signature):
                logger.warning("Invalid webhook signature")
                return HttpResponse("Invalid signature", status=403)

        logger.info("Webhook signature verified successfully")

        # Handle different content types
        if request.content_type == "application/x-www-form-urlencoded":
            # GitHub is sending form-encoded data
            payload_raw = request.POST.get("payload")
            if not payload_raw:
                logger.error("No payload found in form data")
                return HttpResponse("No payload in form data", status=400)

            # Parse the JSON from the payload parameter
            try:
                payload = json.loads(payload_raw)
                logger.info("Successfully parsed form-encoded payload")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse payload JSON: {e}")
                return HttpResponse("Invalid JSON in payload", status=400)

        elif request.content_type == "application/json":
            # Standard JSON webhook
            try:
                payload = json.loads(request.body.decode("utf-8"))
                logger.info("Successfully parsed JSON payload")
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON body: {e}")
                return HttpResponse("Invalid JSON", status=400)
        else:
            logger.error(f"Unsupported content type: {request.content_type}")
            return HttpResponse("Unsupported content type", status=400)

        # Check if it's a push event to main branch
        ref = payload.get("ref")
        logger.info(f"Webhook ref: {ref}")

        if ref == "refs/heads/main":
            logger.info("This is a push to main branch - triggering deployment")

            # Execute your deployment script
            result = subprocess.run(
                ["/home/pen/deploy.sh"],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            if result.returncode == 0:
                logger.info("Deployment script executed successfully")
                logger.info(f"Deployment output: {result.stdout}")
                return HttpResponse("Deployment triggered successfully", status=200)
            else:
                logger.error(f"Deployment script failed: {result.stderr}")
                return HttpResponse(f"Deployment failed: {result.stderr}", status=500)
        else:
            logger.info(f"Not a main branch push (ref: {ref}), skipping deployment")
            return HttpResponse(
                "Webhook received but not a main branch push", status=200
            )

    except subprocess.TimeoutExpired:
        logger.error("Deployment script timed out")
        return HttpResponse("Deployment timed out", status=500)
    except Exception as e:
        logger.error(f"Unexpected webhook error: {str(e)}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        return HttpResponse(f"Webhook processing failed: {str(e)}", status=500)
